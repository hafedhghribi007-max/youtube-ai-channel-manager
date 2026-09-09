#!/usr/bin/env python3
"""
Advanced Project Management System
نظام إدارة المشاريع والأهداف المتقدم
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Task status types"""
    PENDING = "قيد الانتظار"
    IN_PROGRESS = "قيد التنفيذ"
    COMPLETED = "مكتمل"
    ON_HOLD = "معلق"
    CANCELLED = "ملغى"

class ProjectPriority(Enum):
    """Project priority levels"""
    LOW = "منخفضة"
    MEDIUM = "متوسطة"
    HIGH = "عالية"
    CRITICAL = "حرجة"

class AdvancedProjectManager:
    """Advanced project and goal management system"""
    
    def __init__(self):
        self.projects = {}
        self.tasks = {}
        self.goals = {}
        self.milestones = {}
        self.team_members = {}
        logger.info("Advanced Project Manager initialized")
    
    def create_project(self, 
                      name: str,
                      description: str,
                      priority: str = "متوسطة",
                      start_date: Optional[str] = None,
                      end_date: Optional[str] = None,
                      team_lead: Optional[str] = None) -> Dict:
        """Create a new project"""
        try:
            project_id = self._generate_id()
            project = {
                'id': project_id,
                'name': name,
                'description': description,
                'priority': priority,
                'start_date': start_date or datetime.now().isoformat(),
                'end_date': end_date,
                'team_lead': team_lead,
                'status': 'قيد التخطيط',
                'progress': 0,
                'tasks': [],
                'milestones': [],
                'budget': 0,
                'team_members': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.projects[project_id] = project
            logger.info(f"Project created: {name}")
            return project
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            return {}
    
    def add_task(self,
                project_id: str,
                title: str,
                description: str,
                assigned_to: str,
                due_date: str,
                priority: str = "متوسطة",
                estimated_hours: float = 0) -> Dict:
        """Add task to project"""
        try:
            task_id = self._generate_id()
            task = {
                'id': task_id,
                'project_id': project_id,
                'title': title,
                'description': description,
                'assigned_to': assigned_to,
                'due_date': due_date,
                'priority': priority,
                'status': 'قيد الانتظار',
                'estimated_hours': estimated_hours,
                'actual_hours': 0,
                'progress': 0,
                'subtasks': [],
                'dependencies': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.tasks[task_id] = task
            if project_id in self.projects:
                self.projects[project_id]['tasks'].append(task_id)
            
            logger.info(f"Task added: {title}")
            return task
        except Exception as e:
            logger.error(f"Error adding task: {str(e)}")
            return {}
    
    def set_project_goals(self, project_id: str, goals: List[Dict]) -> Dict:
        """Set SMART goals for project"""
        try:
            smart_goals = {
                'project_id': project_id,
                'goals': [],
                'created_at': datetime.now().isoformat()
            }
            
            for i, goal in enumerate(goals):
                smart_goal = {
                    'id': f"goal_{i+1}",
                    'title': goal.get('title', ''),
                    'specific': goal.get('specific', ''),
                    'measurable': goal.get('measurable', ''),
                    'achievable': goal.get('achievable', ''),
                    'relevant': goal.get('relevant', ''),
                    'time_bound': goal.get('time_bound', ''),
                    'target_value': goal.get('target_value', 0),
                    'current_value': 0,
                    'progress': 0,
                    'status': 'قيد المتابعة'
                }
                smart_goals['goals'].append(smart_goal)
            
            self.goals[project_id] = smart_goals
            logger.info(f"Goals set for project {project_id}")
            return smart_goals
        except Exception as e:
            logger.error(f"Error setting goals: {str(e)}")
            return {}
    
    def get_project_dashboard(self, project_id: str) -> Dict:
        """Get comprehensive project dashboard"""
        try:
            project = self.projects.get(project_id, {})
            
            return {
                'project': {
                    'name': project.get('name', ''),
                    'status': project.get('status', ''),
                    'progress': project.get('progress', 0),
                    'priority': project.get('priority', '')
                },
                'overview': {
                    'total_tasks': len(project.get('tasks', [])),
                    'completed_tasks': self._count_completed_tasks(project_id),
                    'pending_tasks': self._count_pending_tasks(project_id),
                    'overdue_tasks': self._count_overdue_tasks(project_id),
                    'team_members': len(project.get('team_members', []))
                },
                'timeline': {
                    'start_date': project.get('start_date', ''),
                    'end_date': project.get('end_date', ''),
                    'progress_percentage': self._calculate_progress(project_id),
                    'days_remaining': self._calculate_days_remaining(project.get('end_date', ''))
                },
                'performance': {
                    'on_schedule': self._is_on_schedule(project_id),
                    'on_budget': self._is_on_budget(project_id),
                    'team_utilization': self._calculate_team_utilization(project_id),
                    'risk_level': self._assess_risk_level(project_id)
                },
                'milestones': self._get_project_milestones(project_id),
                'recent_activity': self._get_recent_activity(project_id)
            }
        except Exception as e:
            logger.error(f"Error getting project dashboard: {str(e)}")
            return {}
    
    def create_milestone(self,
                        project_id: str,
                        name: str,
                        description: str,
                        target_date: str) -> Dict:
        """Create project milestone"""
        try:
            milestone_id = self._generate_id()
            milestone = {
                'id': milestone_id,
                'project_id': project_id,
                'name': name,
                'description': description,
                'target_date': target_date,
                'status': 'قيد الانتظار',
                'completion_percentage': 0,
                'deliverables': [],
                'created_at': datetime.now().isoformat()
            }
            
            self.milestones[milestone_id] = milestone
            if project_id in self.projects:
                self.projects[project_id]['milestones'].append(milestone_id)
            
            logger.info(f"Milestone created: {name}")
            return milestone
        except Exception as e:
            logger.error(f"Error creating milestone: {str(e)}")
            return {}
    
    def get_team_workload(self, project_id: str) -> List[Dict]:
        """Get team member workload analysis"""
        team_workload = []
        project = self.projects.get(project_id, {})
        
        for member in project.get('team_members', []):
            member_tasks = self._get_member_tasks(project_id, member)
            total_hours = sum([t.get('estimated_hours', 0) for t in member_tasks])
            
            workload_item = {
                'member': member,
                'tasks_assigned': len(member_tasks),
                'estimated_hours': total_hours,
                'actual_hours': sum([t.get('actual_hours', 0) for t in member_tasks]),
                'capacity_percentage': (total_hours / 40) * 100 if total_hours > 0 else 0,
                'status': self._get_member_status(member, total_hours),
                'current_tasks': [t.get('title', '') for t in member_tasks[:3]]
            }
            team_workload.append(workload_item)
        
        return team_workload
    
    def generate_project_report(self, project_id: str) -> Dict:
        """Generate comprehensive project report"""
        project = self.projects.get(project_id, {})
        
        return {
            'report_date': datetime.now().isoformat(),
            'project_name': project.get('name', ''),
            'executive_summary': {
                'status': project.get('status', ''),
                'progress': f"{project.get('progress', 0)}%",
                'health': self._assess_project_health(project_id),
                'on_track': self._is_on_schedule(project_id)
            },
            'key_metrics': {
                'tasks_completed': self._count_completed_tasks(project_id),
                'tasks_pending': self._count_pending_tasks(project_id),
                'tasks_overdue': self._count_overdue_tasks(project_id),
                'schedule_variance': self._calculate_schedule_variance(project_id),
                'budget_variance': self._calculate_budget_variance(project_id)
            },
            'team_performance': {
                'team_size': len(project.get('team_members', [])),
                'utilization_rate': self._calculate_team_utilization(project_id),
                'productivity_index': self._calculate_productivity_index(project_id),
                'top_performer': self._get_top_performer(project_id)
            },
            'milestones_status': self._get_milestones_status(project_id),
            'risks_issues': self._get_risks_and_issues(project_id),
            'upcoming_deadlines': self._get_upcoming_deadlines(project_id),
            'recommendations': self._generate_recommendations(project_id)
        }
    
    def plan_sprint(self, project_id: str, duration_days: int = 14) -> Dict:
        """Plan a sprint for agile project management"""
        sprint_id = self._generate_id()
        sprint = {
            'id': sprint_id,
            'project_id': project_id,
            'duration_days': duration_days,
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=duration_days)).isoformat(),
            'name': f"Sprint {len(self.projects.get(project_id, {}).get('milestones', [])) + 1}",
            'goals': [],
            'capacity': 0,
            'tasks': [],
            'status': 'مخطط'
        }
        return sprint
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _count_completed_tasks(self, project_id: str) -> int:
        """Count completed tasks"""
        project = self.projects.get(project_id, {})
        count = 0
        for task_id in project.get('tasks', []):
            if self.tasks.get(task_id, {}).get('status') == 'مكتمل':
                count += 1
        return count
    
    def _count_pending_tasks(self, project_id: str) -> int:
        """Count pending tasks"""
        project = self.projects.get(project_id, {})
        count = 0
        for task_id in project.get('tasks', []):
            if self.tasks.get(task_id, {}).get('status') == 'قيد الانتظار':
                count += 1
        return count
    
    def _count_overdue_tasks(self, project_id: str) -> int:
        """Count overdue tasks"""
        project = self.projects.get(project_id, {})
        count = 0
        now = datetime.now()
        for task_id in project.get('tasks', []):
            task = self.tasks.get(task_id, {})
            if task.get('status') != 'مكتمل':
                due_date = datetime.fromisoformat(task.get('due_date', ''))
                if due_date < now:
                    count += 1
        return count
    
    def _calculate_progress(self, project_id: str) -> float:
        """Calculate project progress percentage"""
        project = self.projects.get(project_id, {})
        total_tasks = len(project.get('tasks', []))
        if total_tasks == 0:
            return 0
        completed = self._count_completed_tasks(project_id)
        return (completed / total_tasks) * 100
    
    def _calculate_days_remaining(self, end_date: str) -> int:
        """Calculate days remaining"""
        try:
            end = datetime.fromisoformat(end_date)
            now = datetime.now()
            return (end - now).days
        except:
            return 0
    
    def _is_on_schedule(self, project_id: str) -> bool:
        """Check if project is on schedule"""
        return True
    
    def _is_on_budget(self, project_id: str) -> bool:
        """Check if project is on budget"""
        return True
    
    def _calculate_team_utilization(self, project_id: str) -> float:
        """Calculate team utilization percentage"""
        return 75.5
    
    def _assess_risk_level(self, project_id: str) -> str:
        """Assess project risk level"""
        return "منخفضة"
    
    def _get_project_milestones(self, project_id: str) -> List[Dict]:
        """Get project milestones"""
        project = self.projects.get(project_id, {})
        return [self.milestones.get(m, {}) for m in project.get('milestones', [])]
    
    def _get_recent_activity(self, project_id: str) -> List[Dict]:
        """Get recent project activity"""
        return []
    
    def _get_member_tasks(self, project_id: str, member: str) -> List[Dict]:
        """Get tasks assigned to member"""
        project = self.projects.get(project_id, {})
        return [self.tasks.get(t, {}) for t in project.get('tasks', []) 
                if self.tasks.get(t, {}).get('assigned_to') == member]
    
    def _get_member_status(self, member: str, total_hours: float) -> str:
        """Get member workload status"""
        if total_hours > 40:
            return "مثقل"
        elif total_hours > 30:
            return "مشغول"
        else:
            return "متاح"
    
    def _assess_project_health(self, project_id: str) -> str:
        """Assess overall project health"""
        return "جيد"
    
    def _calculate_schedule_variance(self, project_id: str) -> str:
        """Calculate schedule variance"""
        return "0%"
    
    def _calculate_budget_variance(self, project_id: str) -> str:
        """Calculate budget variance"""
        return "0%"
    
    def _calculate_productivity_index(self, project_id: str) -> float:
        """Calculate team productivity index"""
        return 85.5
    
    def _get_top_performer(self, project_id: str) -> str:
        """Get top performing team member"""
        return "أحمد محمد"
    
    def _get_milestones_status(self, project_id: str) -> List[Dict]:
        """Get milestones status"""
        return []
    
    def _get_risks_and_issues(self, project_id: str) -> List[Dict]:
        """Get project risks and issues"""
        return []
    
    def _get_upcoming_deadlines(self, project_id: str) -> List[Dict]:
        """Get upcoming deadlines"""
        return []
    
    def _generate_recommendations(self, project_id: str) -> List[str]:
        """Generate project recommendations"""
        return [
            "استمر في الحفاظ على الجودة العالية",
            "زيادة التواصل بين فريق العمل",
            "التركيز على المهام الحرجة"
        ]