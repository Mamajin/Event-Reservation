describe('Navigate to Bookmark Page', () => {
  beforeEach(() => {
    cy.visit('/login');

    cy.get('input[placeholder="Username"]').type('testuser');
    cy.get('input[placeholder="Password"]').type('StrongPass123!');
    cy.get('button').contains('Login').click();

    cy.url().should('not.include', '/login');
  });

  it('should should display bookmarks if exist if non exist then show non', () => {
    cy.contains('Bookmarks').click();
  
    // Verify navigation to the Bookmarks page
    cy.url().should('include', '/bookmarks');
  
    // Check if the "Bookmarked Events" header is visible
    cy.get('h1').contains('Bookmarked Events').should('be.visible');
  
    // Flexible check for empty state or Bookmarks
    cy.get('[data-testid="empty-bookmarks-message"], [data-testid="bookmarks-exist"]')
      .should('exist')
      .then(($el) => {
        if ($el.attr('data-testid') === 'empty-bookmarks-message') {
          cy.wrap($el)
            .should('be.visible')
            .and('contain', "No bookmarked events available");
        } else {
          cy.get('[data-testid="bookmarks-exist"]').should('have.length.gte', 1);
        }
      });
});
});
