REFACTORS for perfect emplamentation: 
  make the conn and reconn the same message sent. Handle reconn vs conn logic on server side by checking if the name is already in the client set
  make seperate locks for each client. Keep a global clientslock then have an attribute for each client be a local lock
  make all varbles based on lists of topics so they can dynamically chnage for fucture emplamentation. 
