describe('Navigate to MyTickets Page', () => {
    beforeEach(() => {
      cy.visit('/login');
  
      cy.get('input[placeholder="Username"]').type('testuser');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
      cy.get('button').contains('Login').click();
  
      cy.url().should('not.include', '/login');
    });
  
    it('should navigate to the MyTickets page from the sidebar', () => {
      cy.contains('My Tickets').click();
  
      // Verify navigation to the Bookmark page
      cy.url().should('include', '/my-tickets');
  
      // Check if the "Bookmarked Events" header is visible
      cy.get('h1').contains('My Tickets').should('be.visible');
  
      // Check if there are any bookmarks or if the empty message is visible
      cy.get('[data-testid="empty-tickets-message"]').then(($message) => {
        if ($message.is(':visible')) {
          // If the empty message is visible, check its text
          cy.wrap($message).should('contain', "You don't have any tickets at the moment.");
        } else {
          // Otherwise, check for bookmark cards
          cy.get('[data-testid="virtual-ticket"]').should('have.length.gte', 0);
        }
      });
    });
  
    it('should display a message if no bookmarks exist', () => {
      // Navigate to the Bookmark page
      cy.contains('My Tickets').click();
  
      // Check if the empty bookmarks message is visible when no bookmarks exist
      cy.get('[data-testid="empty-bookmarks-message"]').should('be.visible')
        .and('contain', "You don't have any tickets at the moment.");
  
      // Ensure no bookmark cards are displayed
      cy.get('.bookmark-card').should('have.length', 0);
    });
  });
  