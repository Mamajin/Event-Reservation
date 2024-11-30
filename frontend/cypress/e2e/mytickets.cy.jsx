describe('Navigate to MyTickets Page', () => {
    beforeEach(() => {
      cy.visit('/login');
  
      cy.get('input[placeholder="Username"]').type('testuser');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
      cy.get('button').contains('Login').click();
  
      cy.url().should('not.include', '/login');
    });
  
    it('should should display tickets if exist if non exist then show non', () => {
        cy.contains('My Tickets').click();
      
        // Verify navigation to the MyTickets page
        cy.url().should('include', '/my-tickets');
      
        // Check if the "My Tickets" header is visible
        cy.get('h1').contains('My Tickets').should('be.visible');
      
        // Flexible check for empty state or tickets
        cy.get('[data-testid="empty-tickets-message"], [data-testid="virtual-ticket-exist"]')
          .should('exist')
          .then(($el) => {
            if ($el.attr('data-testid') === 'empty-tickets-message') {
              cy.wrap($el)
                .should('be.visible')
                .and('contain', "You don't have any tickets at the moment.");
            } else {
              cy.get('[data-testid="virtual-ticket-exist"]').should('have.length.gte', 1);
            }
          });
    });
  });
  