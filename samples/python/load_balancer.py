import heapq
from typing import List, Dict, Any, Optional

class Task:
    def __init__(self, task_id: int, priority: int, duration: int):
        self.task_id = task_id
        self.priority = priority
        self.duration = duration

    def __lt__(self, other):
        # Higher priority value means higher priority (using negative for min-heap)
        return self.priority > other.priority

class LoadBalancer:
    """
    Advanced Simulated Load Balancer Algorithm.
    Distributes tasks across workers based on load and priority.
    Tests: Custom object handling, Priority Queues, Logic Branches.
    """
    def __init__(self, worker_count: int = 3):
        self.worker_count = worker_count
        self.workers = {i: 0 for i in range(worker_count)} # worker_id -> current_load
        self.task_history = []

    def schedule_tasks(self, tasks_data: List[Dict[str, int]], global_limit: int = 100) -> Dict[str, Any]:
        if not tasks_data:
            return {"status": "empty", "assignments": {}}
            
        if self.worker_count <= 0:
            raise ValueError("Worker count must be greater than zero")

        # 1. Initialize Priority Queue (simulated)
        pending = []
        for t in tasks_data:
            # Check for invalid data
            if t.get('duration', 0) < 0 or t.get('priority', 0) < 0:
                continue
            heapq.heappush(pending, (-t['priority'], t['task_id'], t['duration']))

        assignments = {}
        total_processed_load = 0

        # 2. Process tasks
        while pending and total_processed_load < global_limit:
            neg_priority, task_id, duration = heapq.heappop(pending)
            
            # Find the least loaded worker
            best_worker = min(self.workers, key=self.workers.get)
            
            # Application of Logic Branch: Oversized Task Handling
            if duration > 50:
                # Oversized tasks get split or flagged
                status = "oversized_limit"
                self.workers[best_worker] += duration * 1.5 # Heavy penalty
            else:
                status = "standard"
                self.workers[best_worker] += duration

            assignments[task_id] = {
                "worker": best_worker,
                "priority": -neg_priority,
                "complexity": status
            }
            total_processed_load += duration

        # 3. Compile Analytics
        stats = {
            "processed_count": len(assignments),
            "remaining_count": len(pending),
            "worker_distribution": self.workers,
            "system_efficiency": total_processed_load / (self.worker_count * 10) if self.worker_count > 0 else 0
        }
        
        return stats

def run_simulation(tasks: list):
    """Entry point for the AutoTestAI generator"""
    lb = LoadBalancer(worker_count=3)
    return lb.schedule_tasks(tasks, global_limit=200)
