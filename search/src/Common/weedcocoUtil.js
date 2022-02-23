export const parseCategoryName = (categoryName) => {
  const groups = categoryName.match(/^([^:]*): (.*)/);
  console.log('*', groups)
  return groups === null ? {role: categoryName} : {role: groups[1], taxon: groups[2]};
}


