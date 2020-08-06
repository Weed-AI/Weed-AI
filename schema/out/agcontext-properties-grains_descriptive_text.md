# Untitled string in AgContext Schema

```txt
https://weedid.sydney.edu.au/schema/AgContext.json#/properties/grains_descriptive_text
```

Grains descriptive text.
One of ten possible strings describing the crop developmental stage.
If this AgContext is not in a cropping environment, use value "na".


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                              |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ----------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [AgContext.schema.json\*](AgContext.schema.json "open original schema") |

## grains_descriptive_text Type

`string`

## grains_descriptive_text Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value               | Explanation |
| :------------------ | ----------- |
| `"emergence"`       |             |
| `"seedling"`        |             |
| `"tillering"`       |             |
| `"stem_elongation"` |             |
| `"booting"`         |             |
| `"ear_emergence"`   |             |
| `"flowering"`       |             |
| `"milky_dough"`     |             |
| `"dough"`           |             |
| `"ripening"`        |             |
| `"na"`              |             |
