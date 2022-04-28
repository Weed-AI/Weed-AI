const safeSetForm = () => {
	cy.wait(1000)
	// hack needed due to textarea risizing upredictably
	cy.clickText(/JSON data/)
	cy.focused().blur()
	cy.clickText(/^Set Form$/)
}

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
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /WeedCOCO/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_weedcoco/weedcoco.json')
        cy.clickText(/^Next$/)
        cy.get('div.fileContainer > input').attachFile('test_weedcoco/images/001_image.png')
        cy.clickText(/^Submit$/)
    })

    it('Test Weedcoco Zip Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /WeedCOCO/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_weedcoco_zip/weedcoco.json')
        cy.clickText(/^Next$/)
        cy.findAllByText(/^Upload Image Files$/).click()  // select other option in dropdown
        cy.findAllByText(/^Upload Images in Zip$/).click()
        cy.get('input.uppy-Dashboard-input').attachFile('test_weedcoco_zip/weedcoco.zip')
        cy.wait(2000)
        cy.clickText(/^Submit$/)
    })

    it('Test Coco Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /MS COCO/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_coco/coco.json')
        cy.clickText(/^Next$/)
        cy.findByText("crop").type('weed{enter}')
        cy.findByDisplayValue(/^UNSPECIFIED$/).click().clear().type('rapistrum rugosum{enter}')
        cy.clickText(/^Next$/)
        cy.setAgAndMeta()
        cy.get('div.fileContainer > input').attachFile('test_coco/images/002_image.png')
        cy.clickText(/^Submit$/)
    })

    it('Test Voc Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /VOC/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_voc/voc/resizeC1_PLOT_20190728_175852.xml')
        cy.get('.dzu-input').attachFile('test_voc/voc/resizeC1_PLOT_20190728_180135.xml')
        cy.get('.dzu-submitButton').click()
        cy.clickText(/^Next$/)
        cy.clickText(/^Next$/)
        cy.setAgAndMeta()
        cy.get('div.fileContainer > input').attachFile('test_voc/images/resizeC1_PLOT_20190728_175852.jpg')
        cy.get('div.fileContainer > input').attachFile('test_voc/images/resizeC1_PLOT_20190728_180135.jpg')
        cy.clickText(/^Submit$/)
    })

    afterEach(() => {
        cy.findAllByText(/^Log out$/).should('have.length', 1).click()
    })
})
