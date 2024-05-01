import React, { useState } from 'react';
import './App.css';

import axios from 'axios';

function App() {
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('');
  const [urgency, setUrgency] = useState('');
  const [confirmationMessage, setConfirmationMessage] = useState('');
  // eslint-disable-next-line
  const [ticketOutput, setTicketOutput] = useState('');


  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      // Submit ticket to backend
      const response = await axios.post('http://localhost:5000/submitTicket', {
        description,
        category,
        urgency
      });
  
      // Show pop-up message when ticket is submitted successfully
      window.alert('Ticket submitted successfully!');
  
      setConfirmationMessage('Ticket submitted successfully!');
      // Clear form after submission
      setDescription('');
      setCategory('');
      setUrgency('');
  
      // Access the resolution from the response data
      const resolution = response.data.resolution;
      console.log('Resolution:', resolution); // Log the resolution data
      setTicketOutput(resolution);
    } catch (error) {
      console.error('Error submitting ticket:', error);
      setConfirmationMessage('Failed to submit ticket. Please try again later.');
    }
  };
  

  return (
    <div>
      <h1>Ticket Submission Form</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Description:</label><br />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
            cols={50}
            required
          ></textarea>
        </div>
        <div>
          <br />
          <label>Category:</label><br />
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
        </div>
        <div>
          <br />
          <label>Urgency:</label><br />
          <select
            value={urgency}
            onChange={(e) => setUrgency(e.target.value)}
            required
          >
            <option value="">Select urgency</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <br />
        <button type="submit">Submit Ticket</button>
      </form>
      {confirmationMessage && <p>{confirmationMessage}</p>}
    </div>
  );
}

export default App;
