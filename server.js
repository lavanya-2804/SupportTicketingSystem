const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios');
const mongoose = require('mongoose');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// MongoDB Connection
mongoose
  .connect('mongodb://localhost:27017/tickets', {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error(err));

// Ticket Model
const Ticket = mongoose.model('Ticket', {
  description: String,
  category: String,
  urgency: String
});

// Root route handler
app.get('/', (req, res) => {
  res.send('Welcome to the Ticketing System!');
});

// WebSocket setup
const server = http.createServer(app);
const io = socketIo(server);

io.on('connection', socket => {
  console.log('Client connected');

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });

  // Listen for resolution message from ticketing_system.py
  socket.on('resolution', resolution => {
    console.log('Resolution:', resolution);
  });
});

// Endpoint for submitting a ticket
app.post('/submitTicket', async (req, res) => {
  const { description, category, urgency } = req.body;

  try {
    // Create a new Ticket instance
    const ticket = new Ticket({ description, category, urgency });

    // Save ticket to MongoDB
    const savedTicket = await ticket.save();

    // Return ticket ID in the response
    res.json({ message: 'Ticket submitted successfully', ticketId: savedTicket._id });
  } catch (error) {
    console.error('Error submitting ticket:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start the server
server.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
