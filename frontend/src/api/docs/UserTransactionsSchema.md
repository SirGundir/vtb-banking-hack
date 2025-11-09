
# UserTransactionsSchema


## Properties

Name | Type
------------ | -------------
`userId` | number
`status` | string
`currency` | string
`amount` | number
`bookingDt` | Date
`valueDt` | Date
`transactionInfo` | string
`direction` | [TransactionDirection](TransactionDirection.md)

## Example

```typescript
import type { UserTransactionsSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "userId": null,
  "status": null,
  "currency": null,
  "amount": null,
  "bookingDt": null,
  "valueDt": null,
  "transactionInfo": null,
  "direction": null,
} satisfies UserTransactionsSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UserTransactionsSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


