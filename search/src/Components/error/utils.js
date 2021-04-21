export const jsonSchemaTitle = (res) => {
    return `Total ${res.n_errors_found} ${res.n_errors_found > 1? "errors": "error"}`
}

export const jsonSchemaTransform = (details) => {
    const transform = {}
    const pathKey = (path) => `'${path[2]}' field of ${path[0]}`
    for (const error_detail of details.error_details) {
        let path = pathKey(error_detail.path)
        if (path in transform) {
            transform[path].instances.push({path: error_detail.path.join(" / "), message: error_detail.message})
        } else {
            transform[path] = {description: error_detail.schema.description, instances: [{path: error_detail.path.join(" / "), message: error_detail.message}]}
        }
    }
    return transform
}