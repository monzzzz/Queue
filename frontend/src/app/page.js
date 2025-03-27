"use client";

import React, { useEffect, useState } from 'react';
<<<<<<< HEAD
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

=======

function App() {
>>>>>>> 7982ec14162f21bca79bf83a16f23da56669aba2
  return (
    <div>
      
    </div>
  );
}

export default App;