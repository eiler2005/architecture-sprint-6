## Проектирование GraphQL API для InsureTech

### Проблемы текущей реализации REST API
1. **Высокая вариативность данных**: Разные сценарии требуют различные объекты данных (контакты, документы, родственники и т.д.).
2. **Большой объём данных**: Полная карточка клиента может содержать до 500 атрибутов.
3. **Увеличение RPS**: Для одного сценария часто приходится запрашивать несколько объектов данных через разные ресурсы, что кратно увеличивает нагрузку на сервис.
4. **Неоптимальность данных**: Предоставление всех данных клиента через один ресурс невозможно из-за большого объёма и сложности обработки.

### Преимущества использования GraphQL
1. **Гибкость запросов**: Позволяет клиентам выбирать только те данные, которые им необходимы.
2. **Снижение нагрузки на сервер**: Уменьшение количества запросов к API за счёт агрегированных запросов.

Вместо выполнения нескольких REST-запросов (например, /clients/{id}, /clients/{id}/documents, /clients/{id}/relatives), достаточно одного GraphQL-запроса.

Клиент запрашивает только нужные поля (например, только id и name клиента), что уменьшает объем передаваемых данных.

5. **Снижение дублирования**: Устранение избыточных запросов на получение связанных данных.
4. **Упрощение работы с данными**: Предоставление единой точки доступа к различным объектам данных.

### Пример эквивалентной схемы GraphQL
```graphql
type Query {
  client(id: String!): Client
}

type Client {
  id: String!
  name: String
  contacts: [Contact]
  documents: [Document]
  relatives: [Relative]
}

type Contact {
  type: String
  value: String
}

type Document {
  id: String
  name: String
  issuedBy: String
}

type Relative {
  name: String
  relation: String
}
```

### Преимущества предложенной схемы
1. **Универсальность**: Позволяет запрашивать как основные атрибуты клиента, так и связанные данные.
2. **Гибкость**: Пользователь может запрашивать только нужные поля (например, только `name` и `contacts`).
3. **Масштабируемость**: Упрощается добавление новых типов данных в будущем.

### Определите сущности, их поля, а также необходимые запросы (queries), которые покроют все операции REST API.

### Сущности и их поля

#### 1. Client
- `id` (ID клиента, тип: String)
- `name` (Имя клиента, тип: String)
- `contacts` (Контакты, тип: [Contact])
- `documents` (Документы, тип: [Document])
- `relatives` (Родственники, тип: [Relative])

#### 2. Contact
- `type` (Тип контакта, тип: String, например: "email", "phone")
- `value` (Значение контакта, тип: String)

#### 3. Document
- `type` (Тип документа, тип: String, например: "passport", "insurance policy")
- `number` (Номер документа, тип: String)
- `issueDate` (Дата выдачи, тип: String)

#### 4. Relative
- `name` (Имя родственника, тип: String)
- `relation` (Тип родства, тип: String, например: "mother", "sibling")

---

### Необходимые Queries

#### 1. Получить информацию о клиенте по ID
```graphql
query getClient($id: String!) {
  client(id: $id) {
    id
    name
    contacts {
      type
      value
    }
    documents {
      type
      number
      issueDate
    }
    relatives {
      name
      relation
    }
  }
}
```
#### 2. Получить только контакты клиента
```graphql
query getClientContacts($id: String!) {
  client(id: $id) {
    contacts {
      type
      value
    }
  }
}
```

#### 3. Получить только документы клиента
```graphql
query getClientDocuments($id: String!) {
  client(id: $id) {
    documents {
      type
      number
      issueDate
    }
  }
}
```
#### 4. Получить только родственников клиента
```graphql
query getClientRelatives($id: String!) {
  client(id: $id) {
    relatives {
      name
      relation
    }
  }
}
```

### Итоги
Переход на GraphQL позволит InsureTech значительно снизить нагрузку на сервис `client-info`, повысить удобство взаимодействия с данными и упростить поддержку API.
