# Untitled object in undefined Schema

```txt
https://weedid.sydney.edu.au/schema/Collection.json#/allOf/0
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ----------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [Collection.schema.json\*](out/Collection.schema.json "open original schema") |

## 0 Type

`object` ([Details](collection-1-allof-0.md))

# undefined Properties

| Property                          | Type     | Required | Nullable       | Defined by                                                                                                                                                         |
| :-------------------------------- | -------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)                         | `number` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-id.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/id")                         |
| [author](#author)                 | `string` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-author.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/author")                 |
| [title](#title)                   | `string` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-title.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/title")                   |
| [year](#year)                     | `number` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-year.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/year")                     |
| [identifier](#identifier)         | `string` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-identifier.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/identifier")         |
| [rights](#rights)                 | `string` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-rights.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/rights")                 |
| [accrual_policy](#accrual_policy) | `string` | Optional | cannot be null | [Untitled schema](collection-1-allof-0-properties-accrual_policy.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/accrual_policy") |

## id

Identifier for the collection.


`id`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-id.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/id")

### id Type

`number`

## author

Author or authors of the collection the image/annotation belongs to.


`author`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-author.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/author")

### author Type

`string`

## title

Title of the collection.


`title`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-title.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/title")

### title Type

`string`

## year

Collection publication year.


`year`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-year.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/year")

### year Type

`number`

### year Constraints

**maximum**: the value of this number must smaller than or equal to: `3000`

**minimum**: the value of this number must greater than or equal to: `1900`

## identifier

A DOI or other identifier used to find the collection.


`identifier`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-identifier.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/identifier")

### identifier Type

`string`

## rights

Copyright status of the collection.
Further detail available in the licences object.


`rights`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-rights.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/rights")

### rights Type

`string`

## accrual_policy

A description of the accrual policy for this collection.
Open collections can be contributed to, and closed collections cannot be.


`accrual_policy`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Untitled schema](collection-1-allof-0-properties-accrual_policy.md "https&#x3A;//weedid.sydney.edu.au/schema/Collection.json#/allOf/0/properties/accrual_policy")

### accrual_policy Type

`string`

### accrual_policy Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"closed"` |             |
| `"open"`   |             |
