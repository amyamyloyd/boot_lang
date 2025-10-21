import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            Task Manager Dashboard
          </h2>
          <p className="text-gray-600 mb-6">
            Welcome to the Task Manager POC. This is a simple task management system
            demonstrating the tenant isolation pattern.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Link
              to="/tasks"
              className="bg-blue-50 hover:bg-blue-100 p-4 rounded-lg border border-blue-200 transition-colors"
            >
              <h3 className="font-medium text-blue-900">View Tasks</h3>
              <p className="text-sm text-blue-700 mt-1">See all your tasks</p>
            </Link>
            
            <Link
              to="/tasks/new"
              className="bg-green-50 hover:bg-green-100 p-4 rounded-lg border border-green-200 transition-colors"
            >
              <h3 className="font-medium text-green-900">Create Task</h3>
              <p className="text-sm text-green-700 mt-1">Add a new task</p>
            </Link>
            
            <Link
              to="/admin"
              className="bg-purple-50 hover:bg-purple-100 p-4 rounded-lg border border-purple-200 transition-colors"
            >
              <h3 className="font-medium text-purple-900">Admin Panel</h3>
              <p className="text-sm text-purple-700 mt-1">Manage all data</p>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
