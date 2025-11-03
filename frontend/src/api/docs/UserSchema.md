
# UserSchema


## Properties

Name | Type
------------ | -------------
`id` | string
`email` | string
`language` | string
`firstName` | string
`lastName` | string
`emailVerified` | boolean

## Example

```typescript
import type { UserSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "email": null,
  "language": null,
  "firstName": null,
  "lastName": null,
  "emailVerified": null,
} satisfies UserSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


