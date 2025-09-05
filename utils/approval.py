"""
Approval system utility for Personal Automation Agents.
Handles user approval for risky actions before execution.
"""

import time
from typing import Optional, Callable, Any
from config import Config
from utils.logger import AgentLogger
from utils.notifications import NotificationManager

class ApprovalManager:
    """Manages approval workflow for risky automation actions."""
    
    def __init__(self, agent_name: str):
        """
        Initialize approval manager for a specific agent.
        
        Args:
            agent_name: Name of the agent
        """
        self.agent_name = agent_name
        self.logger = AgentLogger(f"approval.{agent_name}")
        self.notifications = NotificationManager(agent_name)
        
        # Pending approvals
        self.pending_approvals = {}
    
    def require_approval(self, action: str, description: str, 
                        data: dict = None, timeout_hours: int = 24) -> bool:
        """
        Check if approval is required for an action.
        
        Args:
            action: Action name (e.g., 'send_email', 'submit_job_application')
            description: Description of what will happen
            data: Additional data about the action
            timeout_hours: Hours to wait for approval before auto-rejecting
            
        Returns:
            bool: True if approval is required, False if not
        """
        # Check configuration for this action type
        if action.startswith('send_email') and Config.REQUIRE_APPROVAL_FOR_EMAILS:
            return True
        elif action.startswith('job_application') and Config.REQUIRE_APPROVAL_FOR_JOB_APPLICATIONS:
            return True
        elif action.startswith('cv_change') and Config.REQUIRE_APPROVAL_FOR_CV_CHANGES:
            return True
        
        return False
    
    def request_approval(self, action: str, description: str, 
                        data: dict = None, timeout_hours: int = 24) -> str:
        """
        Request approval for an action and return approval ID.
        
        Args:
            action: Action name
            description: Description of what will happen
            data: Additional data about the action
            timeout_hours: Hours to wait for approval
            
        Returns:
            str: Approval ID for tracking
        """
        import uuid
        
        approval_id = str(uuid.uuid4())
        timestamp = time.time()
        
        approval_request = {
            'id': approval_id,
            'action': action,
            'description': description,
            'data': data or {},
            'timestamp': timestamp,
            'timeout': timestamp + (timeout_hours * 3600),
            'status': 'pending',
            'response': None
        }
        
        self.pending_approvals[approval_id] = approval_request
        
        # Send notification requesting approval
        self.notifications.warning(
            f"Approval required for: {action}",
            approval_id=approval_id,
            description=description,
            timeout_hours=timeout_hours
        )
        
        self.logger.action("request_approval", target=action, status="sent", approval_id=approval_id)
        
        return approval_id
    
    def check_approval(self, approval_id: str) -> Optional[bool]:
        """
        Check if an approval has been granted or denied.
        
        Args:
            approval_id: Approval ID to check
            
        Returns:
            bool: True if approved, False if denied, None if pending
        """
        if approval_id not in self.pending_approvals:
            return None
        
        approval = self.pending_approvals[approval_id]
        
        # Check timeout
        if time.time() > approval['timeout']:
            approval['status'] = 'timeout'
            approval['response'] = False
            self.logger.warning("Approval timed out", approval_id=approval_id)
        
        if approval['status'] == 'approved':
            return True
        elif approval['status'] == 'denied':
            return False
        elif approval['status'] == 'timeout':
            return False
        
        return None  # Still pending
    
    def approve(self, approval_id: str, user_id: str = "user") -> bool:
        """
        Approve an action.
        
        Args:
            approval_id: Approval ID to approve
            user_id: ID of the user granting approval
            
        Returns:
            bool: True if approval was successful
        """
        if approval_id not in self.pending_approvals:
            self.logger.error("Approval ID not found", approval_id=approval_id)
            return False
        
        approval = self.pending_approvals[approval_id]
        approval['status'] = 'approved'
        approval['response'] = True
        approval['approved_by'] = user_id
        approval['approved_at'] = time.time()
        
        self.logger.action("approve_action", target=approval['action'], status="approved", approval_id=approval_id)
        
        # Send success notification
        self.notifications.success(
            f"Action approved: {approval['action']}",
            approval_id=approval_id,
            approved_by=user_id
        )
        
        return True
    
    def deny(self, approval_id: str, user_id: str = "user", reason: str = None) -> bool:
        """
        Deny an action.
        
        Args:
            approval_id: Approval ID to deny
            user_id: ID of the user denying approval
            reason: Reason for denial
            
        Returns:
            bool: True if denial was successful
        """
        if approval_id not in self.pending_approvals:
            self.logger.error("Approval ID not found", approval_id=approval_id)
            return False
        
        approval = self.pending_approvals[approval_id]
        approval['status'] = 'denied'
        approval['response'] = False
        approval['denied_by'] = user_id
        approval['denied_at'] = time.time()
        approval['denial_reason'] = reason
        
        self.logger.action("deny_action", target=approval['action'], status="denied", approval_id=approval_id, reason=reason)
        
        # Send notification about denial
        self.notifications.warning(
            f"Action denied: {approval['action']}",
            approval_id=approval_id,
            denied_by=user_id,
            reason=reason
        )
        
        return True
    
    def wait_for_approval(self, approval_id: str, check_interval: int = 60) -> bool:
        """
        Wait for approval to be granted or denied.
        
        Args:
            approval_id: Approval ID to wait for
            check_interval: Seconds between approval checks
            
        Returns:
            bool: True if approved, False if denied or timed out
        """
        self.logger.action("wait_for_approval", target=approval_id, status="started")
        
        while True:
            result = self.check_approval(approval_id)
            
            if result is not None:
                self.logger.action("wait_for_approval", target=approval_id, status="completed", result=result)
                return result
            
            time.sleep(check_interval)
    
    def cleanup_expired_approvals(self):
        """Remove expired approvals from memory."""
        current_time = time.time()
        expired_ids = []
        
        for approval_id, approval in self.pending_approvals.items():
            if current_time > approval['timeout'] and approval['status'] == 'pending':
                expired_ids.append(approval_id)
        
        for approval_id in expired_ids:
            del self.pending_approvals[approval_id]
        
        if expired_ids:
            self.logger.info(f"Cleaned up {len(expired_ids)} expired approvals")
    
    def get_pending_approvals(self) -> dict:
        """Get all pending approval requests."""
        return {k: v for k, v in self.pending_approvals.items() if v['status'] == 'pending'}
    
    def get_approval_stats(self) -> dict:
        """Get statistics about approvals."""
        total = len(self.pending_approvals)
        pending = len([a for a in self.pending_approvals.values() if a['status'] == 'pending'])
        approved = len([a for a in self.pending_approvals.values() if a['status'] == 'approved'])
        denied = len([a for a in self.pending_approvals.values() if a['status'] == 'denied'])
        timed_out = len([a for a in self.pending_approvals.values() if a['status'] == 'timeout'])
        
        return {
            'total': total,
            'pending': pending,
            'approved': approved,
            'denied': denied,
            'timed_out': timed_out
        }
