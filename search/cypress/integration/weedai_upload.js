describe('overall upload workflow', () => {

    beforeEach(() => {
        const test_username = `test_${Math.random().toString(36).slice(-4)}`
        const test_password = Math.random().toString(36).slice(-8)
        const test_email = `${test_username}@weed-ai.com`
        cy.visit('http://localhost/upload', {failOnStatusCode: false})
        cy.register(test_username, test_email, test_password)
        cy.login(test_username, test_password)
    })

    it('Test Weedcoco Upload', () => {
        cy.findAllByText(/^Select annotation format$/).should('have.length', 1).type('weedcoco{enter}')
        cy.findAllByText(/^Begin upload$/).should('have.length', 1).click()
        cy.get('.dzu-input').attachFile('test_weedcoco/weedcoco.json')
        cy.findAllByText(/^Next$/).should('have.length', 1).click()
        cy.get('div.fileContainer > input').attachFile('test_weedcoco/images/001_image.png')
        cy.findAllByText(/^Submit$/).should('have.length', 1).click()
    })

    afterEach(() => {
        cy.findAllByText(/^Log out$/).should('have.length', 1).click()
    })
})