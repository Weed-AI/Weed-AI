export const parseCategoryName = (categoryName) => {
  const groups = categoryName.match(/^([^:]*): (.*)/);
  return groups === null ? {role: categoryName} : {role: groups[1], species: groups[2]};
}


