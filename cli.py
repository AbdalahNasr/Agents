#!/usr/bin/env python3
"""
Command Line Interface for Personal Automation Agents

Provides an easy-to-use CLI for interacting with all agents and the notification hub.
"""

import argparse
import sys
import json
from datetime import datetime
from typing import Dict, Any

from config import Config
from agents.email_agent import EmailAgent
from agents.job_agent import JobAgent
from agents.cv_agent import CVAgent
from agents.notification_hub import NotificationHub

class AgentCLI:
    """Command line interface for Personal Automation Agents."""
    
    def __init__(self):
        """Initialize the CLI with all available agents."""
        self.agents = {
            'email': EmailAgent(),
            'job': JobAgent(),
            'cv': CVAgent(),
            'hub': NotificationHub()
        }
        
        # Validate configuration
        missing_config = Config.validate()
        if missing_config:
            print(f"⚠️  Warning: Missing configuration: {', '.join(missing_config)}")
            print("Some features may not work properly. Check your .env file.")
    
    def run(self):
        """Main CLI entry point."""
        parser = argparse.ArgumentParser(
            description="Personal Automation Agents CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Process emails from last 24 hours
  python cli.py email process --hours 24
  
  # Search for jobs and create applications
  python cli.py job search --max-apps 10
  
  # Enhance CV for software engineer role
  python cli.py cv enhance --role "Software Engineer" --input cv.txt
  
  # Start monitoring hub
  python cli.py hub start
  
  # Get system status
  python cli.py hub status
            """
        )
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Email agent commands
        email_parser = subparsers.add_parser('email', help='Email Agent commands')
        email_subparsers = email_parser.add_subparsers(dest='email_command')
        
        email_process_parser = email_subparsers.add_parser('process', help='Process inbox')
        email_process_parser.add_argument('--hours', type=int, default=24, help='Hours back to process')
        
        # Job agent commands
        job_parser = subparsers.add_parser('job', help='Job Application Agent commands')
        job_subparsers = job_parser.add_subparsers(dest='job_command')
        
        job_search_parser = job_subparsers.add_parser('search', help='Search for jobs')
        job_search_parser.add_argument('--max-apps', type=int, default=5, help='Maximum applications to create')
        job_search_parser.add_argument('--location', default='remote', help='Job location preference')
        
        # CV agent commands
        cv_parser = subparsers.add_parser('cv', help='CV Enhancement Agent commands')
        cv_subparsers = cv_parser.add_subparsers(dest='cv_command')
        
        cv_enhance_parser = cv_subparsers.add_parser('enhance', help='Enhance CV')
        cv_enhance_parser.add_argument('--role', required=True, help='Target job role')
        cv_enhance_parser.add_argument('--input', help='Input CV file (or use --text)')
        cv_enhance_parser.add_argument('--text', help='CV text content')
        cv_enhance_parser.add_argument('--job-desc', help='Job description for customization')
        
        # Hub commands
        hub_parser = subparsers.add_parser('hub', help='Notification Hub commands')
        hub_subparsers = hub_parser.add_subparsers(dest='hub_command')
        
        hub_start_parser = hub_subparsers.add_parser('start', help='Start monitoring hub')
        hub_stop_parser = hub_subparsers.add_parser('stop', help='Stop monitoring hub')
        hub_status_parser = hub_subparsers.add_parser('status', help='Get system status')
        hub_run_parser = hub_subparsers.add_parser('run', help='Run agent manually')
        hub_run_parser.add_argument('agent', help='Agent name to run')
        hub_run_parser.add_argument('--params', help='JSON parameters for the agent')
        
        # Parse arguments
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        # Execute command
        try:
            self._execute_command(args)
        except KeyboardInterrupt:
            print("\n🛑 Operation cancelled by user")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)
    
    def _execute_command(self, args):
        """Execute the parsed command."""
        if args.command == 'email':
            self._handle_email_command(args)
        elif args.command == 'job':
            self._handle_job_command(args)
        elif args.command == 'cv':
            self._handle_cv_command(args)
        elif args.command == 'hub':
            self._handle_hub_command(args)
        else:
            print(f"❌ Unknown command: {args.command}")
    
    def _handle_email_command(self, args):
        """Handle email agent commands."""
        if args.email_command == 'process':
            print(f"📧 Processing emails from last {args.hours} hours...")
            result = self.agents['email'].process_inbox(args.hours)
            
            if result.get('success'):
                print(f"✅ Email processing completed!")
                print(f"📊 Processed {result.get('emails_processed', 0)} emails")
                print(f"⏱️  Duration: {result.get('duration', 0):.2f}s")
                
                if 'summary' in result:
                    summary = result['summary']
                    print(f"\n📋 Summary:")
                    for category, count in summary.get('categories', {}).items():
                        emoji = {'work': '💼', 'personal': '👤', 'spam': '🚫', 'unknown': '❓'}
                        print(f"  {emoji.get(category, '📧')} {category.title()}: {count}")
                    
                    if summary.get('important', 0) > 0:
                        print(f"  ⚠️  Important: {summary['important']}")
            else:
                print(f"❌ Email processing failed: {result.get('error', 'Unknown error')}")
    
    def _handle_job_command(self, args):
        """Handle job agent commands."""
        if args.job_command == 'search':
            print(f"💼 Searching for jobs and creating applications...")
            result = self.agents['job'].process_applications(args.max_apps)
            
            if result.get('success'):
                print(f"✅ Job processing completed!")
                print(f"📊 Found {result.get('jobs_found', 0)} jobs")
                print(f"📝 Created {result.get('applications_created', 0)} applications")
                print(f"⏱️  Duration: {result.get('duration', 0):.2f}s")
                
                # Show application stats
                stats = self.agents['job'].get_application_stats()
                print(f"\n📈 Application Stats:")
                print(f"  Total: {stats['total']}")
                print(f"  Drafts: {stats['drafts']}")
                print(f"  Submitted: {stats['submitted']}")
            else:
                print(f"❌ Job processing failed: {result.get('error', 'Unknown error')}")
    
    def _handle_cv_command(self, args):
        """Handle CV agent commands."""
        if args.cv_command == 'enhance':
            # Get CV text
            cv_text = None
            if args.input:
                try:
                    with open(args.input, 'r', encoding='utf-8') as f:
                        cv_text = f.read()
                except FileNotFoundError:
                    print(f"❌ File not found: {args.input}")
                    return
                except Exception as e:
                    print(f"❌ Error reading file: {str(e)}")
                    return
            elif args.text:
                cv_text = args.text
            else:
                print("❌ Please provide either --input file or --text content")
                return
            
            print(f"📝 Enhancing CV for {args.role} role...")
            result = self.agents['cv'].enhance_cv(
                cv_text=cv_text,
                job_description=args.job_desc,
                target_role=args.role
            )
            
            if 'error' not in result:
                print(f"✅ CV enhancement completed!")
                print(f"📊 Enhanced {len(result.get('enhanced_sections', {}))} sections")
                print(f"🔄 Created {len(result.get('versions', []))} versions")
                print(f"💡 Generated {len(result.get('suggestions', []))} suggestions")
                
                # Show enhancement example
                if 'enhanced_sections' in result and 'summary' in result['enhanced_sections']:
                    summary = result['enhanced_sections']['summary']
                    print(f"\n📋 Summary Enhancement Example:")
                    print(f"Original: {summary['original'][:100]}...")
                    print(f"Enhanced: {summary['enhanced'][:100]}...")
                
                # Show some suggestions
                if result.get('suggestions'):
                    print(f"\n💡 Top Suggestions:")
                    for i, suggestion in enumerate(result['suggestions'][:3], 1):
                        print(f"  {i}. {suggestion}")
            else:
                print(f"❌ CV enhancement failed: {result.get('error', 'Unknown error')}")
    
    def _handle_hub_command(self, args):
        """Handle hub commands."""
        hub = self.agents['hub']
        
        if args.hub_command == 'start':
            print("🎯 Starting Notification Hub...")
            hub.start_monitoring()
            print("✅ Hub started successfully!")
            print("📊 Monitoring all agents...")
            print("🔄 Press Ctrl+C to stop")
            
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping hub...")
                hub.stop_monitoring()
                print("✅ Hub stopped")
        
        elif args.hub_command == 'stop':
            print("🛑 Stopping Notification Hub...")
            hub.stop_monitoring()
            print("✅ Hub stopped")
        
        elif args.hub_command == 'status':
            print("📊 Getting system status...")
            status = hub.get_system_health()
            agent_status = hub.get_agent_status()
            performance = hub.get_performance_summary()
            
            print(f"\n🏥 System Health: {status['status'].upper()}")
            print(f"📈 Overall Success Rate: {status['overall_success_rate']:.1f}%")
            print(f"🔄 Monitoring Active: {'Yes' if status['monitoring_active'] else 'No'}")
            
            print(f"\n🤖 Agent Status:")
            for agent_name, agent_info in agent_status.items():
                emoji = {
                    'running': '🟢',
                    'idle': '🟡',
                    'error': '🔴',
                    'stopped': '⚫'
                }
                status_emoji = emoji.get(agent_info['status'], '❓')
                print(f"  {status_emoji} {agent_name}: {agent_info['status']}")
                if agent_info['last_run']:
                    last_run = datetime.fromisoformat(agent_info['last_run'])
                    print(f"    Last run: {last_run.strftime('%Y-%m-%d %H:%M:%S')}")
                if agent_info['success_count'] > 0 or agent_info['error_count'] > 0:
                    print(f"    Success: {agent_info['success_count']}, Errors: {agent_info['error_count']}")
            
            print(f"\n📊 Performance (Last 24h):")
            print(f"  Total Runs: {performance['total_runs']}")
            print(f"  Success Rate: {performance['success_rate']:.1f}%")
            print(f"  Avg Duration: {performance['avg_duration']:.2f}s")
        
        elif args.hub_command == 'run':
            print(f"🚀 Running {args.agent} manually...")
            
            # Parse parameters if provided
            params = {}
            if args.params:
                try:
                    params = json.loads(args.params)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON parameters")
                    return
            
            result = hub.run_agent_manual(args.agent, **params)
            
            if result.get('success'):
                print(f"✅ {args.agent} completed successfully!")
                # Show result summary
                if 'emails_processed' in result:
                    print(f"📧 Processed {result['emails_processed']} emails")
                if 'jobs_found' in result:
                    print(f"💼 Found {result['jobs_found']} jobs")
                if 'sections_enhanced' in result:
                    print(f"📝 Enhanced {result['sections_enhanced']} CV sections")
            else:
                print(f"❌ {args.agent} failed: {result.get('error', 'Unknown error')}")


def main():
    """Main entry point."""
    cli = AgentCLI()
    cli.run()


if __name__ == "__main__":
    main()
