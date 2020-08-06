# AgContext Schema

```txt
https://weedid.sydney.edu.au/schema/AgContext.json
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [AgContext.schema.json](out/AgContext.schema.json "open original schema") |

## AgContext Type

`object` ([AgContext](agcontext-1.md))

# AgContext Properties

| Property                                            | Type      | Required | Nullable       | Defined by                                                                                                                                                   |
| :-------------------------------------------------- | --------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)                                           | `number`  | Required | cannot be null | [AgContext](agcontext-1-properties-id.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/id")                                           |
| [crop_type](#crop_type)                             | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-crop_type.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/crop_type")                             |
| [grains_descriptive_text](#grains_descriptive_text) | `string`  | Optional | cannot be null | [AgContext](agcontext-1-properties-grains_descriptive_text.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/grains_descriptive_text") |
| [bbch_descriptive_text](#bbch_descriptive_text)     | `string`  | Optional | cannot be null | [AgContext](agcontext-1-properties-bbch_descriptive_text.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/bbch_descriptive_text")     |
| [bbch_code](#bbch_code)                             | `string`  | Optional | cannot be null | [AgContext](agcontext-1-properties-bbch_code.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/bbch_code")                             |
| [soil_colour](#soil_colour)                         | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-soil_colour.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/soil_colour")                         |
| [surface_cover](#surface_cover)                     | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-surface_cover.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/surface_cover")                     |
| [surface_coverage](#surface_coverage)               | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-surface_coverage.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/surface_coverage")               |
| [weather_description](#weather_description)         | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-weather_description.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/weather_description")         |
| [location_lat](#location_lat)                       | `number`  | Required | cannot be null | [AgContext](agcontext-1-properties-location_lat.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/location_lat")                       |
| [location_long](#location_long)                     | `number`  | Required | cannot be null | [AgContext](agcontext-1-properties-location_long.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/location_long")                     |
| [location_datum](#location_datum)                   | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-location_datum.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/location_datum")                   |
| [camera_type](#camera_type)                         | Merged    | Optional | cannot be null | [AgContext](agcontext-1-properties-camera_type.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_type")                         |
| [camera_height](#camera_height)                     | Merged    | Required | cannot be null | [AgContext](agcontext-1-properties-camera_height.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_height")                     |
| [camera_angle](#camera_angle)                       | Merged    | Required | cannot be null | [AgContext](agcontext-1-properties-camera_angle.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_angle")                       |
| [camera_fov](#camera_fov)                           | Merged    | Required | cannot be null | [AgContext](agcontext-1-properties-camera_fov.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_fov")                           |
| [photography_description](#photography_description) | `string`  | Required | cannot be null | [AgContext](agcontext-1-properties-photography_description.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/photography_description") |
| [cropped_to_plant](#cropped_to_plant)               | `boolean` | Required | cannot be null | [AgContext](agcontext-1-properties-cropped_to_plant.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/cropped_to_plant")               |

## id

A number identifying the AgContext.


`id`

-   is required
-   Type: `number`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-id.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/id")

### id Type

`number`

## crop_type

General crop type.
A string describing the general cropping scenario (e.g. "root vegetable").


`crop_type`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-crop_type.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/crop_type")

### crop_type Type

`string`

## grains_descriptive_text

Grains descriptive text.
One of ten possible strings describing the crop developmental stage.
If this AgContext is not in a cropping environment, use value "na".


`grains_descriptive_text`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-grains_descriptive_text.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/grains_descriptive_text")

### grains_descriptive_text Type

`string`

### grains_descriptive_text Constraints

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

## bbch_descriptive_text

BBCG descriptive text.
One of several possible strings describing the stage of the crop, chosen from a list of possible terms used by the BBCH.
If this AgContext is not in a cropping environment, use value "na".


`bbch_descriptive_text`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-bbch_descriptive_text.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/bbch_descriptive_text")

### bbch_descriptive_text Type

`string`

### bbch_descriptive_text Constraints

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

## bbch_code

BBCG descriptive text.
One of several possible strings describing the stage of the crop, chosen from a list of codes used by the BBCH.
If this AgContext is not in a cropping environment, use value "na".


`bbch_code`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-bbch_code.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/bbch_code")

### bbch_code Type

`string`

### bbch_code Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | ----------- |
| `"gs01"` |             |
| `"gs02"` |             |
| `"gs04"` |             |
| `"gs05"` |             |
| `"gs06"` |             |
| `"gs07"` |             |
| `"gs08"` |             |
| `"gs09"` |             |
| `"gs10"` |             |
| `"gs11"` |             |
| `"gs12"` |             |
| `"gs13"` |             |
| `"gs14"` |             |
| `"gs15"` |             |
| `"gs16"` |             |
| `"gs17"` |             |
| `"gs18"` |             |
| `"gs19"` |             |
| `"gs20"` |             |
| `"gs21"` |             |
| `"gs22"` |             |
| `"gs23"` |             |
| `"gs24"` |             |
| `"gs25"` |             |
| `"gs26"` |             |
| `"gs27"` |             |
| `"gs28"` |             |
| `"gs29"` |             |
| `"gs30"` |             |
| `"gs31"` |             |
| `"gs32"` |             |
| `"gs33"` |             |
| `"gs34"` |             |
| `"gs35"` |             |
| `"gs36"` |             |
| `"gs37"` |             |
| `"gs38"` |             |
| `"gs39"` |             |
| `"gs40"` |             |
| `"gs41"` |             |
| `"gs42"` |             |
| `"gs43"` |             |
| `"gs44"` |             |
| `"gs45"` |             |
| `"gs46"` |             |
| `"gs47"` |             |
| `"gs48"` |             |
| `"gs49"` |             |
| `"gs50"` |             |
| `"gs51"` |             |
| `"gs52"` |             |
| `"gs53"` |             |
| `"gs54"` |             |
| `"gs55"` |             |
| `"gs56"` |             |
| `"gs57"` |             |
| `"gs58"` |             |
| `"gs59"` |             |
| `"gs60"` |             |
| `"gs61"` |             |
| `"gs62"` |             |
| `"gs63"` |             |
| `"gs64"` |             |
| `"gs65"` |             |
| `"gs66"` |             |
| `"gs67"` |             |
| `"gs68"` |             |
| `"gs69"` |             |
| `"gs70"` |             |
| `"gs71"` |             |
| `"gs72"` |             |
| `"gs73"` |             |
| `"gs74"` |             |
| `"gs75"` |             |
| `"gs76"` |             |
| `"gs77"` |             |
| `"gs78"` |             |
| `"gs79"` |             |
| `"gs80"` |             |
| `"gs81"` |             |
| `"gs82"` |             |
| `"gs83"` |             |
| `"gs84"` |             |
| `"gs85"` |             |
| `"gs86"` |             |
| `"gs87"` |             |
| `"gs88"` |             |
| `"gs89"` |             |
| `"gs90"` |             |
| `"gs91"` |             |
| `"gs92"` |             |
| `"gs93"` |             |
| `"gs94"` |             |
| `"gs95"` |             |
| `"gs96"` |             |
| `"gs97"` |             |
| `"gs98"` |             |
| `"gs99"` |             |

## soil_colour

Soil colour.
General description of the soil colour.


`soil_colour`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-soil_colour.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/soil_colour")

### soil_colour Type

`string`

### soil_colour Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value           | Explanation |
| :-------------- | ----------- |
| `"not_visible"` |             |
| `"black"`       |             |
| `"dark_brown"`  |             |
| `"brown"`       |             |
| `"red_brown"`   |             |
| `"dark_red"`    |             |
| `"yellow"`      |             |
| `"pale_yellow"` |             |
| `"white"`       |             |
| `"grey"`        |             |

## surface_cover

Surface cover type.
One of several strings describing the background cover that is behind any plants in the images.


`surface_cover`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-surface_cover.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/surface_cover")

### surface_cover Type

`string`

### surface_cover Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value             | Explanation |
| :---------------- | ----------- |
| `"cereal"`        |             |
| `"oilseed"`       |             |
| `"legume"`        |             |
| `"cotton"`        |             |
| `"black_plastic"` |             |
| `"white_plastic"` |             |
| `"woodchips"`     |             |
| `"other"`         |             |

## surface_coverage

Percent of coverage in image.
Approximate measurement of the percent of the soil in the image that is covered by the surface cover.


`surface_coverage`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-surface_coverage.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/surface_coverage")

### surface_coverage Type

`string`

### surface_coverage Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"0-25"`   |             |
| `"25-50"`  |             |
| `"50-75"`  |             |
| `"75-100"` |             |

## weather_description

Weather conditions in images.
Free text description of approximate weather conditions during the image capture session.


`weather_description`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-weather_description.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/weather_description")

### weather_description Type

`string`

## location_lat

Latitude in decimal degrees. Approximate latitude location of the AgContext, in decimal degrees.


`location_lat`

-   is required
-   Type: `number`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-location_lat.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/location_lat")

### location_lat Type

`number`

## location_long

Longitude in decimal degrees. Approximate longitude location of the AgContext, in decimal degrees.


`location_long`

-   is required
-   Type: `number`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-location_long.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/location_long")

### location_long Type

`number`

## location_datum

EPSG code of spatial datum.
A numeric string indicting the EPSG code for the spatial reference system used for the location of the AgContext.


`location_datum`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-location_datum.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/location_datum")

### location_datum Type

`string`

## camera_type

Type of camera.
Free text denoting the model/make of camera used for this AgContext.
If this is not fixed within the AgContext, use value "variable".


`camera_type`

-   is optional
-   Type: merged type ([Details](agcontext-1-properties-camera_type.md))
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-camera_type.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_type")

### camera_type Type

merged type ([Details](agcontext-1-properties-camera_type.md))

any of

-   [Untitled string in AgContext](agcontext-1-properties-camera_type-anyof-0.md "check type definition")
-   [Untitled string in AgContext](agcontext-1-properties-camera_type-anyof-1.md "check type definition")

## camera_height

Height of camera.
An number representing the height of the camera, measured in millimeters .
If this is not fixed within the AgContext, use value "variable".


`camera_height`

-   is required
-   Type: merged type ([Details](agcontext-1-properties-camera_height.md))
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-camera_height.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_height")

### camera_height Type

merged type ([Details](agcontext-1-properties-camera_height.md))

any of

-   [Untitled number in AgContext](agcontext-1-properties-camera_height-anyof-0.md "check type definition")
-   [Untitled string in AgContext](agcontext-1-properties-camera_height-anyof-1.md "check type definition")

## camera_angle

Angle of camera. A number representing the angle at which the camera is positioned, in degrees. A camera facing straight down would be 90. If this is not fixed within the AgContext, use value "variable".


`camera_angle`

-   is required
-   Type: merged type ([Details](agcontext-1-properties-camera_angle.md))
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-camera_angle.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_angle")

### camera_angle Type

merged type ([Details](agcontext-1-properties-camera_angle.md))

any of

-   [Untitled number in AgContext](agcontext-1-properties-camera_angle-anyof-0.md "check type definition")
-   [Untitled string in AgContext](agcontext-1-properties-camera_angle-anyof-1.md "check type definition")

## camera_fov

Field of view for camera.
A number representing the angle captured by the camera across the diagonal of an image, measured in degrees.
If this is not fixed within the AgContext, use value "variable".


`camera_fov`

-   is required
-   Type: merged type ([Details](agcontext-1-properties-camera_fov.md))
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-camera_fov.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/camera_fov")

### camera_fov Type

merged type ([Details](agcontext-1-properties-camera_fov.md))

any of

-   [Untitled number in AgContext](agcontext-1-properties-camera_fov-anyof-0.md "check type definition")
-   [Untitled string in AgContext](agcontext-1-properties-camera_fov-anyof-1.md "check type definition")

## photography_description

Description of photography. Free text description of salient aspects of camera, mount and lighting.


`photography_description`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-photography_description.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/photography_description")

### photography_description Type

`string`

## cropped_to_plant

Has the image been cropped to the plant? A boolean indicating if the image has been cropped to the plant.


`cropped_to_plant`

-   is required
-   Type: `boolean`
-   cannot be null
-   defined in: [AgContext](agcontext-1-properties-cropped_to_plant.md "https&#x3A;//weedid.sydney.edu.au/schema/AgContext.json#/properties/cropped_to_plant")

### cropped_to_plant Type

`boolean`
