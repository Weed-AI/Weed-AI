describe('Test the overallworkflow', () => {

    beforeEach(() => {
        cy.visit('http://localhost/upload', {failOnStatusCode: false})

        const test_username = 'admin_test'
        const test_password = 'password_test'
        const test_email = 'admin_test@weed-ai.com'

        cy.findAllByText(/^Sign up$/).should('have.length', 1).click()
        cy.get('#username')
          .type(test_username)
          .should('have.value', test_username)
        cy.get('#password')
          .type(test_password)
          .should('have.value', test_password)
        cy.get('#email')
          .type(test_email)
          .should('have.value', test_email)
        cy.findAllByRole('button', /^Sign Up$/).should('have.length', 1).click()

        cy.findAllByText(/^Sign In$/).should('have.length', 1).click()
        cy.get('#username')
          .type(test_username)
          .should('have.value', test_username)
        cy.get('#password')
          .type(test_password)
          .should('have.value', test_password)
        cy.findAllByRole('button', /^Sign In$/).should('have.length', 1).click()
    })

    it('Test Weedcoco Upload', () => {
        cy.findAllByText(/^Select annotation format$/).should('have.length', 1).type('weedcoco{enter}')
        cy.findAllByText(/^Begin upload$/).should('have.length', 1).click()
        cy.get('.dzu-input').attachFile('test_weedcoco/weedcoco.json')
        cy.findAllByText(/^Next$/).should('have.length', 1).click()
        cy.get('div.fileContainer > input').attachFile('test_weedcoco/images/001_image.png')
        cy.findAllByText(/^Submit$/).should('have.length', 1).click()
    })

    // it('Test Coco Upload', () => {

    // })

    afterEach(() => {
        cy.findAllByText(/^Log out$/).should('have.length', 1).click()
    })
})