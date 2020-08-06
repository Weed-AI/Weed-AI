# Untitled string in AgContext Schema

```txt
https://weedid.sydney.edu.au/schema/AgContext.json#/properties/bbch_descriptive_text
```

BBCG descriptive text.
One of several possible strings describing the stage of the crop, chosen from a list of possible terms used by the BBCH.
If this AgContext is not in a cropping environment, use value "na".


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                              |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ----------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [AgContext.schema.json\*](AgContext.schema.json "open original schema") |

## bbch_descriptive_text Type

`string`

## bbch_descriptive_text Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value                                           | Explanation |
| :---------------------------------------------- | ----------- |
| `"germination"`                                 |             |
| `"sprouting"`                                   |             |
| `"bud development"`                             |             |
| `"leaf development"`                            |             |
| `"formation of side shoots"`                    |             |
| `"tillering"`                                   |             |
| `"stem elongation"`                             |             |
| `"rosette growth"`                              |             |
| `"shoot development"`                           |             |
| `"development of harvestable vegetative parts"` |             |
| `"bolting"`                                     |             |
| `"inflorescence emergence"`                     |             |
| `"heading"`                                     |             |
| `"flowering"`                                   |             |
| `"development of fruit"`                        |             |
| `"ripening or maturity of fruit and seed"`      |             |
| `"senescence"`                                  |             |
| `"beginning of dormancy"`                       |             |
| `"na"`                                          |             |
