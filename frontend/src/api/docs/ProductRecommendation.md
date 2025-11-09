
# ProductRecommendation


## Properties

Name | Type
------------ | -------------
`productId` | string
`productType` | string
`productName` | string
`description` | string
`interestRate` | number
`minAmount` | number
`maxAmount` | number
`termMonths` | number
`bank` | string
`notes` | string

## Example

```typescript
import type { ProductRecommendation } from ''

// TODO: Update the object below with actual values
const example = {
  "productId": null,
  "productType": null,
  "productName": null,
  "description": null,
  "interestRate": null,
  "minAmount": null,
  "maxAmount": null,
  "termMonths": null,
  "bank": null,
  "notes": null,
} satisfies ProductRecommendation

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ProductRecommendation
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


