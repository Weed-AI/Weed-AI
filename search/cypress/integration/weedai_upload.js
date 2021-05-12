describe('Test the overallworkflow', function () {

    beforeEach(() => {
        cy.visit('http://localhost/upload', {failOnStatusCode: false})
        cy.findAllByText(/^Sign In$/).should('have.length', 1).click()
        // Below works for Username still with id but can't find Password for some reason, so I decided to keep using id for the fields
        // cy.findAllByRole('textbox', {name: 'Username'}).should('have.length', 1).type('admin').should('have.value', 'admin').tab()
        // cy.findAllByRole('textbox', {name: 'Password'}).should('have.length', 1).type('password').should('have.value', 'password')
        cy.get('#username')
          .type('admin')
          .should('have.value', 'admin')
        cy.get('#password')
          .type('password')
          .should('have.value', 'password')
        cy.findAllByRole('button', /^Sign In$/).should('have.length', 1).click()
    })

    it('Test Weedcoco Upload', function () {
        cy.findAllByText(/^Select annotation format$/).should('have.length', 1).type('weedcoco{enter}')
        cy.findAllByText(/^Begin upload$/).should('have.length', 1).click()
        cy.get('.dzu-input').attachFile('test_weedcoco/weedcoco.json')
        cy.findAllByText(/^Next$/).should('have.length', 1).click()
        cy.get('div.fileContainer > input').attachFile('test_weedcoco/images/001_image.png')
        cy.findAllByText(/^Submit$/).should('have.length', 1).click()
        cy.findAllByText(/^Log out$/).should('have.length', 1).click()
    })

})