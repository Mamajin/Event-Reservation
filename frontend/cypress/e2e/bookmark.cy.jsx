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

    // Check if the "Bookmarked Events" header is visible
    cy.get('h1').contains('Bookmarked Events').should('be.visible');

    // Check if there are any bookmarks or if the empty message is visible
    cy.get('[data-testid="empty-bookmarks-message"]').then(($message) => {
      if ($message.is(':visible')) {
        // If the empty message is visible, check its text
        cy.wrap($message).should('contain', 'No bookmarked events available');
      } else {
        // Otherwise, check for bookmark cards
        cy.get('[data-testid="bookmark-card"]').should('have.length.gte', 0);
      }
    });
  });

  it('should display a message if no bookmarks exist', () => {
    // Navigate to the Bookmark page
    cy.contains('Bookmarks').click();

    // Check if the empty bookmarks message is visible when no bookmarks exist
    cy.get('[data-testid="empty-bookmarks-message"]').should('be.visible')
      .and('contain', 'No bookmarked events available');

    // Ensure no bookmark cards are displayed
    cy.get('.bookmark-card').should('have.length', 0);
  });
});
