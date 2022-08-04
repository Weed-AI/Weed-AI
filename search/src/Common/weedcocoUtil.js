export const parseCategoryName = (categoryName) => {
  const groups = categoryName.match(/^([^:]*): ([^\(]*)(?: \((.*?)\))?/);
  return groups === null ? {role: categoryName} : {role: groups[1], taxon: groups[2], subcategory: groups[3]};
}

export const formatCategoryName = ({ role, taxon, subcategory }) => {
  return `${role || '??'}: ${taxon || '??'}${subcategory ? " (" + subcategory + ')' : ""}`
}