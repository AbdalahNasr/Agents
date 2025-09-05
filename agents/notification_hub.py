"""
Notification Hub - Central Agent Coordinator

This agent serves as a central hub that connects all automation agents and provides
a unified interface for managing notifications, approvals, and agent coordination.

Features:
- Centralizes notifications from all agents
- Manages approval workflows across agents
- Provides agent status monitoring and health checks
- Schedules and coordinates agent execution
- Maintains unified logging and reporting
- Web interface for monitoring and control

Usage:
    python agents/notification_hub.py
    
    # Or import and use programmatically:
    from agents.notification_hub import NotificationHub
    hub = NotificationHub()
    hub.start_monitoring()
"""

import time
import json
import schedule
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from config import Config
from utils.logger import AgentLogger
from utils.notifications import NotificationManager
from utils.approval import ApprovalManager

# Import agents
from agents.email_agent import EmailAgent
from agents.job_agent import JobAgent
from agents.cv_agent import CVAgent

@dataclass
class AgentStatus:
    """Data class for tracking agent status."""
    name: str
    status: str  # 'running', 'stopped', 'error', 'idle'
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    success_count: int
    error_count: int
    last_error: Optional[str]
    performance_metrics: Dict[str, Any]

class NotificationHub:
    """Central hub for coordinating all automation agents."""
    
    def __init__(self):
        """Initialize the Notification Hub with all agents and monitoring systems."""
        self.logger = AgentLogger("notification_hub")
        self.notifications = NotificationManager("notification_hub")
        self.approval = ApprovalManager("notification_hub")
        
        # Initialize agents
        self.agents = {
            'email_agent': EmailAgent(),
            'job_agent': JobAgent(),
            'cv_agent': CVAgent()
        }
        
        # Agent status tracking
        self.agent_status = {}
        self.initialize_agent_status()
        
        # Monitoring and scheduling
        self.monitoring_active = False
        self.scheduler_thread = None
        
        # Performance tracking
        self.performance_history = []
        self.max_history_size = 1000
        
        # Configuration
        self.schedule_config = {
            'email_agent': {'frequency': '2h', 'enabled': True},
            'job_agent': {'frequency': '6h', 'enabled': True},
            'cv_agent': {'frequency': 'manual', 'enabled': False}  # CV agent runs on demand
        }
        
        self.logger.info("Notification Hub initialized", agents=list(self.agents.keys()))
    
    def initialize_agent_status(self):
        """Initialize status tracking for all agents."""
        for agent_name in self.agents.keys():
            self.agent_status[agent_name] = AgentStatus(
                name=agent_name,
                status='idle',
                last_run=None,
                next_run=None,
                success_count=0,
                error_count=0,
                last_error=None,
                performance_metrics={}
            )
    
    def start_monitoring(self):
        """Start the monitoring and scheduling system."""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        try:
            self.logger.action("start_monitoring", target="all_agents", status="started")
            
            # Setup scheduled tasks
            self._setup_schedules()
            
            # Start monitoring thread
            self.monitoring_active = True
            self.scheduler_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.scheduler_thread.start()
            
            self.notifications.success("Notification Hub monitoring started successfully")
            self.logger.action("start_monitoring", target="all_agents", status="completed")
            
        except Exception as e:
            self.logger.error("Failed to start monitoring", error=e)
            self.notifications.error(f"Failed to start monitoring: {str(e)}")
    
    def stop_monitoring(self):
        """Stop the monitoring and scheduling system."""
        if not self.monitoring_active:
            return
        
        try:
            self.logger.action("stop_monitoring", target="all_agents", status="started")
            
            self.monitoring_active = False
            
            # Clear all schedules
            schedule.clear()
            
            # Wait for monitoring thread to finish
            if self.scheduler_thread and self.scheduler_thread.is_alive():
                self.scheduler_thread.join(timeout=5)
            
            self.notifications.info("Notification Hub monitoring stopped")
            self.logger.action("stop_monitoring", target="all_agents", status="completed")
            
        except Exception as e:
            self.logger.error("Failed to stop monitoring", error=e)
    
    def _setup_schedules(self):
        """Setup scheduled tasks for all agents."""
        for agent_name, config in self.schedule_config.items():
            if config['enabled'] and config['frequency'] != 'manual':
                self._schedule_agent(agent_name, config['frequency'])
    
    def _schedule_agent(self, agent_name: str, frequency: str):
        """Schedule an agent to run at specified frequency."""
        try:
            if frequency == '1h':
                schedule.every().hour.do(self._run_agent, agent_name)
            elif frequency == '2h':
                schedule.every(2).hours.do(self._run_agent, agent_name)
            elif frequency == '6h':
                schedule.every(6).hours.do(self._run_agent, agent_name)
            elif frequency == '12h':
                schedule.every(12).hours.do(self._run_agent, agent_name)
            elif frequency == 'daily':
                schedule.every().day.at("09:00").do(self._run_agent, agent_name)
            else:
                self.logger.warning(f"Unknown frequency for {agent_name}: {frequency}")
                return
            
            self.logger.info(f"Scheduled {agent_name} to run {frequency}")
            
            # Update next run time
            if hasattr(schedule, 'next_run'):
                self.agent_status[agent_name].next_run = schedule.next_run()
            
        except Exception as e:
            self.logger.error(f"Failed to schedule {agent_name}", error=e)
    
    def _monitoring_loop(self):
        """Main monitoring loop that runs scheduled tasks."""
        self.logger.info("Monitoring loop started")
        
        while self.monitoring_active:
            try:
                # Run pending scheduled tasks
                schedule.run_pending()
                
                # Check agent health
                self._check_agent_health()
                
                # Cleanup old performance data
                self._cleanup_performance_history()
                
                # Sleep for a short interval
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error("Error in monitoring loop", error=e)
                time.sleep(60)  # Wait longer on error
        
        self.logger.info("Monitoring loop stopped")
    
    def _run_agent(self, agent_name: str):
        """Run a specific agent and track its performance."""
        if agent_name not in self.agents:
            self.logger.error(f"Unknown agent: {agent_name}")
            return
        
        try:
            self.logger.action("run_agent", target=agent_name, status="started")
            
            # Update status
            self.agent_status[agent_name].status = 'running'
            self.agent_status[agent_name].last_run = datetime.now()
            
            # Run agent based on type
            start_time = time.time()
            result = self._execute_agent(agent_name)
            duration = time.time() - start_time
            
            # Update status based on result
            if result and result.get('success', False):
                self.agent_status[agent_name].status = 'idle'
                self.agent_status[agent_name].success_count += 1
                self.logger.action("run_agent", target=agent_name, status="completed")
            else:
                self.agent_status[agent_name].status = 'error'
                self.agent_status[agent_name].error_count += 1
                self.agent_status[agent_name].last_error = result.get('error', 'Unknown error') if result else 'No result'
                self.logger.action("run_agent", target=agent_name, status="failed")
            
            # Record performance metrics
            self._record_performance(agent_name, duration, result)
            
            # Update next run time
            self._update_next_run_time(agent_name)
            
        except Exception as e:
            self.logger.error(f"Failed to run {agent_name}", error=e)
            self.agent_status[agent_name].status = 'error'
            self.agent_status[agent_name].error_count += 1
            self.agent_status[agent_name].last_error = str(e)
    
    def _execute_agent(self, agent_name: str) -> Optional[Dict]:
        """Execute a specific agent's main functionality."""
        agent = self.agents[agent_name]
        
        try:
            if agent_name == 'email_agent':
                return agent.process_inbox()
            elif agent_name == 'job_agent':
                return agent.process_applications()
            elif agent_name == 'cv_agent':
                # CV agent doesn't have a scheduled task, return success
                return {'success': True, 'message': 'CV agent ready for manual use'}
            else:
                self.logger.error(f"Unknown agent execution method for {agent_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Agent execution failed for {agent_name}", error=e)
            return {'success': False, 'error': str(e)}
    
    def _record_performance(self, agent_name: str, duration: float, result: Dict):
        """Record performance metrics for an agent run."""
        performance_record = {
            'agent_name': agent_name,
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'success': result.get('success', False) if result else False,
            'result_summary': self._summarize_result(result) if result else 'No result'
        }
        
        self.performance_history.append(performance_record)
        
        # Update agent status metrics
        if agent_name in self.agent_status:
            self.agent_status[agent_name].performance_metrics = {
                'last_duration': duration,
                'avg_duration': self._calculate_avg_duration(agent_name),
                'success_rate': self._calculate_success_rate(agent_name)
            }
    
    def _summarize_result(self, result: Dict) -> str:
        """Create a summary of agent execution result."""
        if not result:
            return 'No result'
        
        if result.get('success', False):
            summary_parts = []
            
            if 'emails_processed' in result:
                summary_parts.append(f"{result['emails_processed']} emails")
            if 'jobs_found' in result:
                summary_parts.append(f"{result['jobs_found']} jobs")
            if 'sections_enhanced' in result:
                summary_parts.append(f"{result['sections_enhanced']} CV sections")
            
            return f"Success: {', '.join(summary_parts)}" if summary_parts else "Success"
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    
    def _calculate_avg_duration(self, agent_name: str) -> float:
        """Calculate average execution duration for an agent."""
        agent_records = [r for r in self.performance_history if r['agent_name'] == agent_name]
        if not agent_records:
            return 0.0
        
        total_duration = sum(r['duration'] for r in agent_records)
        return total_duration / len(agent_records)
    
    def _calculate_success_rate(self, agent_name: str) -> float:
        """Calculate success rate for an agent."""
        agent_records = [r for r in self.performance_history if r['agent_name'] == agent_name]
        if not agent_records:
            return 0.0
        
        success_count = sum(1 for r in agent_records if r['success'])
        return (success_count / len(agent_records)) * 100
    
    def _update_next_run_time(self, agent_name: str):
        """Update the next scheduled run time for an agent."""
        try:
            # Get the next scheduled run
            job = schedule.get_jobs(agent_name)
            if job:
                self.agent_status[agent_name].next_run = job[0].next_run
        except Exception as e:
            self.logger.warning(f"Could not update next run time for {agent_name}", error=str(e))
    
    def _check_agent_health(self):
        """Check health of all agents and send alerts if needed."""
        for agent_name, status in self.agent_status.items():
            # Check for agents stuck in error state
            if status.status == 'error' and status.error_count > 3:
                self.notifications.warning(
                    f"Agent {agent_name} has encountered multiple errors",
                    error_count=status.error_count,
                    last_error=status.last_error
                )
            
            # Check for agents that haven't run recently
            if status.last_run and status.status != 'error':
                time_since_last_run = datetime.now() - status.last_run
                if time_since_last_run > timedelta(hours=24):
                    self.notifications.warning(
                        f"Agent {agent_name} hasn't run recently",
                        hours_since_last_run=time_since_last_run.total_seconds() / 3600
                    )
    
    def _cleanup_performance_history(self):
        """Remove old performance records to prevent memory bloat."""
        if len(self.performance_history) > self.max_history_size:
            # Keep only the most recent records
            self.performance_history = self.performance_history[-self.max_history_size:]
    
    def run_agent_manual(self, agent_name: str, **kwargs) -> Dict:
        """
        Manually run an agent with optional parameters.
        
        Args:
            agent_name: Name of the agent to run
            **kwargs: Additional parameters for the agent
            
        Returns:
            Dict: Execution result
        """
        if agent_name not in self.agents:
            return {'success': False, 'error': f'Unknown agent: {agent_name}'}
        
        try:
            self.logger.action("manual_run", target=agent_name, status="started")
            
            # Update status
            self.agent_status[agent_name].status = 'running'
            self.agent_status[agent_name].last_run = datetime.now()
            
            # Execute agent
            start_time = time.time()
            result = self._execute_agent_manual(agent_name, **kwargs)
            duration = time.time() - start_time
            
            # Update status
            if result and result.get('success', False):
                self.agent_status[agent_name].status = 'idle'
                self.agent_status[agent_name].success_count += 1
            else:
                self.agent_status[agent_name].status = 'error'
                self.agent_status[agent_name].error_count += 1
                self.agent_status[agent_name].last_error = result.get('error', 'Unknown error') if result else 'No result'
            
            # Record performance
            self._record_performance(agent_name, duration, result)
            
            self.logger.action("manual_run", target=agent_name, status="completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Manual run failed for {agent_name}", error=e)
            return {'success': False, 'error': str(e)}
    
    def _execute_agent_manual(self, agent_name: str, **kwargs) -> Dict:
        """Execute agent with manual parameters."""
        agent = self.agents[agent_name]
        
        try:
            if agent_name == 'email_agent':
                hours_back = kwargs.get('hours_back', 24)
                return agent.process_inbox(hours_back)
            
            elif agent_name == 'job_agent':
                max_applications = kwargs.get('max_applications', 5)
                return agent.process_applications(max_applications)
            
            elif agent_name == 'cv_agent':
                cv_text = kwargs.get('cv_text')
                job_description = kwargs.get('job_description')
                target_role = kwargs.get('target_role')
                
                if not cv_text:
                    return {'success': False, 'error': 'CV text is required'}
                
                return agent.enhance_cv(cv_text, job_description, target_role=target_role)
            
            else:
                return {'success': False, 'error': f'Unknown agent: {agent_name}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_agent_status(self) -> Dict[str, Dict]:
        """Get current status of all agents."""
        return {name: asdict(status) for name, status in self.agent_status.items()}
    
    def get_performance_summary(self, hours: int = 24) -> Dict:
        """Get performance summary for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_records = [
            r for r in self.performance_history
            if datetime.fromisoformat(r['timestamp']) > cutoff_time
        ]
        
        if not recent_records:
            return {'total_runs': 0, 'success_rate': 0, 'avg_duration': 0}
        
        total_runs = len(recent_records)
        success_count = sum(1 for r in recent_records if r['success'])
        success_rate = (success_count / total_runs) * 100
        avg_duration = sum(r['duration'] for r in recent_records) / total_runs
        
        return {
            'total_runs': total_runs,
            'success_rate': success_rate,
            'avg_duration': avg_duration,
            'period_hours': hours
        }
    
    def get_pending_approvals(self) -> Dict:
        """Get all pending approvals across all agents."""
        all_approvals = {}
        
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'approval'):
                agent_approvals = agent.approval.get_pending_approvals()
                if agent_approvals:
                    all_approvals[agent_name] = agent_approvals
        
        return all_approvals
    
    def approve_action(self, agent_name: str, approval_id: str, user_id: str = "user") -> bool:
        """Approve an action for a specific agent."""
        if agent_name not in self.agents:
            return False
        
        agent = self.agents[agent_name]
        if hasattr(agent, 'approval'):
            return agent.approval.approve(approval_id, user_id)
        
        return False
    
    def deny_action(self, agent_name: str, approval_id: str, user_id: str = "user", reason: str = None) -> bool:
        """Deny an action for a specific agent."""
        if agent_name not in self.agents:
            return False
        
        agent = self.agents[agent_name]
        if hasattr(agent, 'approval'):
            return agent.approval.deny(approval_id, user_id, reason)
        
        return False
    
    def get_system_health(self) -> Dict:
        """Get overall system health status."""
        total_agents = len(self.agents)
        running_agents = sum(1 for status in self.agent_status.values() if status.status == 'running')
        error_agents = sum(1 for status in self.agent_status.values() if status.status == 'error')
        idle_agents = sum(1 for status in self.agent_status.values() if status.status == 'idle')
        
        # Calculate overall success rate
        total_runs = sum(status.success_count + status.error_count for status in self.agent_status.values())
        if total_runs > 0:
            overall_success_rate = (
                sum(status.success_count for status in self.agent_status.values()) / total_runs
            ) * 100
        else:
            overall_success_rate = 100
        
        return {
            'status': 'healthy' if error_agents == 0 else 'degraded' if error_agents < total_agents else 'unhealthy',
            'total_agents': total_agents,
            'running_agents': running_agents,
            'error_agents': error_agents,
            'idle_agents': idle_agents,
            'overall_success_rate': overall_success_rate,
            'monitoring_active': self.monitoring_active,
            'last_updated': datetime.now().isoformat()
        }


def main():
    """Main function to run the Notification Hub standalone."""
    print("🚀 Starting Notification Hub...")
    
    # Validate configuration
    missing_config = Config.validate()
    if missing_config:
        print(f"❌ Missing configuration: {', '.join(missing_config)}")
        print("Please check your .env file and env_example.txt for required values.")
        return
    
    # Create and start hub
    hub = NotificationHub()
    
    try:
        # Start monitoring
        hub.start_monitoring()
        
        print("✅ Notification Hub started successfully!")
        print("📊 Monitoring all agents...")
        print("🔄 Press Ctrl+C to stop")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping Notification Hub...")
        hub.stop_monitoring()
        print("✅ Notification Hub stopped")


if __name__ == "__main__":
    main()
