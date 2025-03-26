"use client";

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';

const socket = io('http://192.168.1.127:5000');

function App() {
  const [preparingTasks, setPreparingTasks] = useState([]);
  const [finishedTasks, setFinishedTasks] = useState([]);
  const [formData, setFormData] = useState({ category: 'BK', prefix: 'PM', number: '' });

  useEffect(() => {
    loadTasks();

    socket.on('update_tasks', (data) => {
      setPreparingTasks(data.preparing);
      setFinishedTasks(data.finished);
    });

    return () => {
      socket.disconnect(); // Clean up on unmount
    };
  }, []);

  const loadTasks = async () => {
    const response = await axios.get('http://192.168.1.127:5000/tasks');
    setPreparingTasks(response.data.preparing);
    setFinishedTasks(response.data.finished);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const addTask = async () => {
    if (!formData.category || !formData.prefix || !formData.number) {
      alert('Please fill out all fields.');
      return;
    }
    await axios.post('http://192.168.1.127:5000/tasks', formData);
    setFormData({ category: 'BK', prefix: 'PM', number: '' });
  };

  const finishTask = async (taskId) => {
    await axios.post('http://192.168.1.127:5000/tasks/finish', { task_id: taskId });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-4xl font-bold mb-6 text-center text-red-600">Queue System</h2>

      {/* ✅ Add Task Form */}
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md mb-8">
        <h3 className="text-2xl font-semibold mb-4 text-gray-700">➕ Add Order</h3>
        <div className="flex gap-4">
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="border rounded-lg p-3 w-full"
          >
            <option value="BK">BK</option>
            <option value="CS">CS</option>
          </select>
          <select
            name="prefix"
            value={formData.prefix}
            onChange={handleChange}
            className="border rounded-lg p-3 w-full"
          >
            <option value="PM">PM</option>
            <option value="JN">JN</option>
            <option value="SM">SM</option>
          </select>
          <input
            type="text"
            name="number"
            value={formData.number}
            onChange={handleChange}
            placeholder="4-digit number"
            className="border rounded-lg p-3 w-full"
          />
          <button
            onClick={addTask}
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition"
          >
            Add Task
          </button>
        </div>
      </div>

      {/* ✅ Side-by-Side Queue Display */}
      <div className="grid grid-cols-2 gap-6">
        {/* 🟡 Preparing Queue */}
        <div className="bg-yellow-50 p-6 rounded-lg shadow-md">
          <h3 className="text-2xl font-semibold mb-4 text-yellow-700">🕒 Preparing Queue</h3>
          <div className="grid grid-cols-2 gap-4 overflow-y-auto max-h-[500px]">
            {preparingTasks?.map((task, index) => (
              <div key={index} className="bg-white border rounded-lg p-4 shadow-md flex justify-between items-center">
                <div>
                  <span className="block font-bold text-xl">{`${task.category}${task.prefix}/${task.number}`}</span>
                  <span className="block text-sm text-gray-400">
                    Created at: {new Date(task.created_at).toLocaleString()}
                  </span>
                </div>
                <button
                  onClick={() => finishTask(task.task_id)}
                  className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
                >
                  ✅ Finish
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* ✅ Finished Queue */}
        <div className="bg-green-50 p-6 rounded-lg shadow-md">
          <h3 className="text-2xl font-semibold mb-4 text-green-700">✅ Finished Queue</h3>
          <div className="grid grid-cols-2 gap-4 overflow-y-auto max-h-[500px]">
            {finishedTasks?.map((task, index) => (
              <div key={index} className="bg-white border rounded-lg p-4 shadow-md">
                <div>
                  <span className="block font-bold text-xl">{`${task.category}${task.prefix}/${task.number}`}</span>
                  <span className="block text-sm text-gray-400">
                    Created at: {new Date(task.created_at).toLocaleString()}
                  </span>
                  <span className="block text-sm text-gray-400">
                    Finished at: {task.finished_at ? new Date(task.finished_at).toLocaleString() : 'Not finished'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;