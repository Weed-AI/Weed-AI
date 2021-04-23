export const jsonSchemaTitle = (res) => {
    return `Total ${res.n_errors_found} ${res.n_errors_found > 1? "errors": "error"}`
}

export const jsonSchemaTransform = (details) => {
    const transform = {}
    const pathKey = (path) => path.length === 1 ?
                              path[0] :
                              path.length === 2 ?
                              `'${path[1]}' field of ${path[0]}` :
                              path.length === 3 ?
                              `'${path[2]}' field of ${path[1]} in ${path[0]}` :
                              path.join(".")
    for (const error_detail of details.error_details) {
        let namedPaths = error_detail.path.filter(word => typeof word == typeof '')
        let path = pathKey(namedPaths)
        if (!(path in transform)) {
            transform[path] = {description: error_detail.schema.description, instances: []}
        }
        transform[path].instances.push({path: error_detail.path.join("."), message: error_detail.message});
    }
    return transform
}