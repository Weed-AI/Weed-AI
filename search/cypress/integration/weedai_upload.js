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
        cy.click_text(/^Begin upload$/)
        cy.get('.dzu-input').attachFile('test_weedcoco/weedcoco.json')
        cy.click_text(/^Next$/)
        cy.get('div.fileContainer > input').attachFile('test_weedcoco/images/001_image.png')
        cy.click_text(/^Submit$/)
    })

    it('Test Coco Upload', () => {
        cy.findAllByText(/^Select annotation format$/).should('have.length', 1).type('coco{enter}')
        cy.click_text(/^Begin upload$/)
        cy.get('.dzu-input').attachFile('test_coco/weedcoco.json')
        cy.click_text(/^Next$/)
        cy.click_text(/^Apply$/)
        cy.click_text(/^Next$/)
        cy.click_text(/^Upload and Download Form Contents$/)
        cy.get('.dzu-input').attachFile('test_coco/agcontext.json')
        cy.wait(2000)
        cy.click_text(/^Set Form$/)
        cy.click_text(/^Next$/)
        cy.click_text(/^Upload and Download Form Contents$/)
        cy.get('.dzu-input').attachFile('test_coco/metadata.json')
        cy.wait(2000)
        cy.click_text(/^Set Form$/)
        cy.click_text(/^Next$/)
        cy.get('div.fileContainer > input').attachFile('test_coco/images/002_image.png')
        cy.click_text(/^Submit$/)
    })

    it('Test Voc Upload', () => {
        cy.findAllByText(/^Select annotation format$/).should('have.length', 1).type('voc{enter}')
        cy.click_text(/^Begin upload$/)
        cy.get('.dzu-input').attachFile('test_voc/voc/resizeC1_PLOT_20190728_175852.xml')
        cy.get('.dzu-input').attachFile('test_voc/voc/resizeC1_PLOT_20190728_180135.xml')
        cy.get('.dzu-submitButton').click()
        cy.click_text(/^Next$/)
        cy.click_text(/^Apply$/)
        cy.click_text(/^Next$/)
        cy.click_text(/^Upload and Download Form Contents$/)
        cy.get('.dzu-input').attachFile('test_voc/agcontext.json')
        cy.wait(2000)
        cy.click_text(/^Set Form$/)
        cy.click_text(/^Next$/)
        cy.click_text(/^Upload and Download Form Contents$/)
        cy.get('.dzu-input').attachFile('test_voc/metadata.json')
        cy.wait(2000)
        cy.click_text(/^Set Form$/)
        cy.click_text(/^Next$/)
        cy.get('div.fileContainer > input').attachFile('test_voc/images/resizeC1_PLOT_20190728_175852.jpg')
        cy.get('div.fileContainer > input').attachFile('test_voc/images/resizeC1_PLOT_20190728_180135.jpg')
        cy.click_text(/^Submit$/)
    })

    afterEach(() => {
        cy.findAllByText(/^Log out$/).should('have.length', 1).click()
    })
})