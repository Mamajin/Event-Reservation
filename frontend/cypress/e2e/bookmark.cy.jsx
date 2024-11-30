describe('Navigate to Bookmark Page', () => {
    beforeEach(() => {
      cy.visit('/login');
  
      cy.get('input[placeholder="Username"]').type('testuser');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
      cy.get('button').contains('Login').click();
  
      cy.url().should('not.include', '/login');
    });
  
    it('should navigate to the Bookmark page from the sidebar', () => {
      cy.contains('Bookmarks').click();
  
      // Verify navigation to the Bookmark page
      cy.url().should('include', '/bookmarks');
  
      // Check for expected elements on the Bookmark page
      cy.get('h1').contains('Bookmarked Events').should('be.visible');
      cy.get('.bookmark-card').should('have.length.gte', 0);
    });
  
    it('should display a message if no bookmarks exist', () => {
      // Navigate to the Bookmark page
      cy.contains('Bookmarks').click();
  
      // Check for empty bookmarks message
      cy.get('[data-testid="empty-bookmarks-message"]')
        .should('be.visible')
        .and('contain', 'No bookmarked events available');
    });
  });
  