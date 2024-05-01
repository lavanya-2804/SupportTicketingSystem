import React from 'react';

const TicketDetails = ({ ticketId, resolution }) => {
  return (
    <div>
      <h2>Ticket Details</h2>
      <p>Ticket ID: {ticketId}</p>
      <p>Resolution: {resolution}</p>
      {/* Add more details as needed */}
    </div>
  );
};

export default TicketDetails;
