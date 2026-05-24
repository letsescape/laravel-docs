# プロンプト (Prompts)

- [Introduction](#introduction)
- [Installation](#installation)
- [利用可能なプロンプト](#available-prompts)
    - [Text](#text)
    - [Textarea](#textarea)
    - [Number](#number)
    - [Password](#password)
    - [Confirm](#confirm)
    - [Select](#select)
    - [Multi-select](#multiselect)
    - [Suggest](#suggest)
    - [Search](#search)
    - [Multi-search](#multisearch)
    - [Pause](#pause)
- [検証前の入力の変換](#transforming-input-before-validation)
- [Forms](#forms)
- [情報メッセージ](#informational-messages)
- [Tables](#tables)
- [Spin](#spin)
- [プログレスバー](#progress)
- [ターミナルのクリア](#clear)
- [端末に関する考慮事項](#terminal-considerations)
- [サポートされていない環境とフォールバック](#fallbacks)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravelプロンプト](https://github.com/laravel/prompts) は、プレースホルダー テキストや検証などのブラウザーのような機能を備えた、美しくユーザーフレンドリーなフォームをコマンドライン アプリケーションに追加するための PHP パッケージです。

<img src="https://laravel.com/img/docs/prompts-example.png">

Laravel プロンプトは、[Artisan コンソールコマンド](/docs/{{version}}/artisan#writing-commands) でユーザー入力を受け入れるのに最適ですが、コマンドライン PHP プロジェクトでも使用できます。

> [!NOTE]
> Laravel プロンプトは、WSL を使用して macOS、Linux、および Windows をサポートします。詳細については、[サポートされていない環境とフォールバック](#fallbacks) のドキュメントを参照してください。

<a name="installation"></a>
## インストール (Installation)

Laravel Prompts は、Laravel の最新リリースにすでに含まれています。

Laravel プロンプトは、Composer パッケージ マネージャーを使用して他の PHP プロジェクトにインストールすることもできます。

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 利用可能なプロンプト (Available Prompts)

<a name="text"></a>
### 文章

`text` 関数は、ユーザーに指定された質問を表示し、入力を受け入れて、それを返します。

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

プレースホルダー テキスト、デフォルト値、情報ヒントを含めることもできます。

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 必須の値

値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 追加の検証

最後に、追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

あるいは、Laravel の [validator](/docs/{{version}}/validation) の機能を活用することもできます。これを行うには、属性の名前と必要な検証ルールを含む配列を `validate` 引数に指定します。

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### テキストエリア

`textarea` 関数は、ユーザーに指定された質問を表示し、複数行のテキストエリアを介して入力を受け入れ、それを返します。

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

プレースホルダー テキスト、デフォルト値、情報ヒントを含めることもできます。

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 必須の値

値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 追加の検証

最後に、追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: fn (string $value) => match (true) {
        strlen($value) < 250 => 'The story must be at least 250 characters.',
        strlen($value) > 10000 => 'The story must not exceed 10,000 characters.',
        default => null
    }
);
```

クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

あるいは、Laravel の [validator](/docs/{{version}}/validation) の機能を活用することもできます。これを行うには、属性の名前と必要な検証ルールを含む配列を `validate` 引数に指定します。

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="number"></a>
### 番号

`number` 関数は、ユーザーに指定された質問を表示し、数値入力を受け入れて、それを返します。 `number` 関数を使用すると、ユーザーは上下の矢印キーを使用して数値を操作できます。

```php
use function Laravel\Prompts\number;

$number = number('How many copies would you like?');
```

プレースホルダー テキスト、デフォルト値、情報ヒントを含めることもできます。

```php
$name = number(
    label: 'How many copies would you like?',
    placeholder: '5',
    default: 1,
    hint: 'This will be determine how many copies to create.'
);
```

<a name="number-required"></a>
#### 必須の値

値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$copies = number(
    label: 'How many copies would you like?',
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$copies = number(
    label: 'How many copies would you like?',
    required: 'A number of copies is required.'
);
```

<a name="number-validation"></a>
#### 追加の検証

最後に、追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: fn (?int $value) => match (true) {
        $value < 1 => 'At least one copy is required.',
        $value > 100 => 'You may not create more than 100 copies.',
        default => null
    }
);
```

クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

あるいは、Laravel の [validator](/docs/{{version}}/validation) の機能を活用することもできます。これを行うには、属性の名前と必要な検証ルールを含む配列を `validate` 引数に指定します。

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: ['copies' => 'required|integer|min:1|max:100']
);
```

<a name="password"></a>
### パスワード

`password` 関数は `text` 関数に似ていますが、ユーザーの入力はコンソールに入力するときにマスクされます。これは、パスワードなどの機密情報を要求する場合に役立ちます。

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

プレースホルダー テキストと情報ヒントを含めることもできます。

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 必須の値

値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 追加の検証

最後に、追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

あるいは、Laravel の [validator](/docs/{{version}}/validation) の機能を活用することもできます。これを行うには、属性の名前と必要な検証ルールを含む配列を `validate` 引数に指定します。

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 確認する

ユーザーに「はいまたはいいえ」の確認を求める必要がある場合は、`confirm` 関数を使用できます。ユーザーは矢印キーを使用するか、`y` または `n` を押して応答を選択できます。この関数は、`true` または `false` を返します。

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

デフォルト値、「はい」と「いいえ」ラベルのカスタマイズされた文言、および情報ヒントを含めることもできます。

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    default: false,
    yes: 'I accept',
    no: 'I decline',
    hint: 'The terms must be accepted to continue.'
);
```

<a name="confirm-required"></a>
#### 「はい」を要求する

必要に応じて、`required` 引数を渡して、ユーザーに「はい」を選択するよう要求することもできます。

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 選択

ユーザーに事前定義された一連の選択肢から選択する必要がある場合は、`select` 関数を使用できます。

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

デフォルトの選択と情報ヒントを指定することもできます。

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

連想配列を `options` 引数に渡して、値の代わりに選択したキーを返すようにすることもできます。

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    default: 'owner'
);
```

リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を渡すことでこれをカスタマイズできます。

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 追加の検証

他のプロンプト関数とは異なり、`select` 関数は何も選択できないため、`required` 引数を受け入れません。ただし、オプションを提示する必要があるが選択されないようにする場合は、`validate` 引数にクロージャーを渡すことができます。

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    validate: fn (string $value) =>
        $value === 'owner' && User::where('role', 'owner')->exists()
            ? 'An owner already exists.'
            : null
);
```

`options` 引数が連想配列の場合、クロージャは選択されたキーを受け取り、それ以外の場合は選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="multiselect"></a>
### 複数選択

ユーザーが複数のオプションを選択できるようにする必要がある場合は、`multiselect` 関数を使用できます。

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

デフォルトの選択肢と情報ヒントを指定することもできます。

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

連想配列を `options` 引数に渡して、選択したオプションの値の代わりにキーを返すこともできます。

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    default: ['read', 'create']
);
```

リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を渡すことでこれをカスタマイズできます。

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 値の要求

デフォルトでは、ユーザーは 0 個以上のオプションを選択できます。代わりに、`required` 引数を渡して 1 つ以上のオプションを適用できます。

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、`required` 引数に文字列を指定できます。

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 追加の検証

オプションを提示する必要があるが、それが選択されないようにする場合は、`validate` 引数にクロージャーを渡すことができます。

```php
$permissions = multiselect(
    label: 'What permissions should the user have?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    validate: fn (array $values) => ! in_array('read', $values)
        ? 'All users require the read permission.'
        : null
);
```

`options` 引数が連想配列の場合、クロージャは選択されたキーを受け取り、それ以外の場合は選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="suggest"></a>
### 提案する

`suggest` 関数を使用すると、可能な選択肢のオートコンプリートを提供できます。ユーザーは、オートコンプリートのヒントに関係なく、任意の回答を入力できます。

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

あるいは、`suggest` 関数の 2 番目の引数としてクロージャを渡すこともできます。クロージャは、ユーザーが入力文字を入力するたびに呼び出されます。クロージャは、これまでのユーザーの入力を含む文字列パラメータを受け入れ、オートコンプリートのオプションの配列を返す必要があります。

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

プレースホルダー テキスト、デフォルト値、情報ヒントを含めることもできます。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    placeholder: 'E.g. Taylor',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="suggest-required"></a>
#### 必須の値

値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 追加の検証

最後に、追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

あるいは、Laravel の [validator](/docs/{{version}}/validation) の機能を活用することもできます。これを行うには、属性の名前と必要な検証ルールを含む配列を `validate` 引数に指定します。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 検索

ユーザーが選択できるオプションが多数ある場合、`search` 関数を使用すると、ユーザーは矢印キーを使用してオプションを選択する前に、検索クエリを入力して結果をフィルタリングできます。

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

クロージャは、ユーザーがこれまでに入力したテキストを受け取り、オプションの配列を返す必要があります。連想配列を返す場合は、選択したオプションのキーが返され、それ以外の場合は、代わりにその値が返されます。

値を返す配列をフィルタリングする場合は、配列が結合しないように `array_values` 関数または `values` Collection メソッドを使用する必要があります。

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

プレースホルダー テキストと情報ヒントを含めることもできます。

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を渡すことでこれをカスタマイズできます。

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-validation"></a>
#### 追加の検証

追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return 'This user has opted-out of receiving mail.';
        }
    }
);
```

`options` クロージャが連想配列を返す場合、クロージャは選択されたキーを受け取り、そうでない場合は、選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="multisearch"></a>
### 複数検索

検索可能なオプションが多数あり、ユーザーが複数の項目を選択できるようにする必要がある場合、`multisearch` 関数を使用すると、ユーザーは矢印キーとスペースバーを使用してオプションを選択する前に、検索クエリを入力して結果をフィルタリングできます。

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

クロージャは、ユーザーがこれまでに入力したテキストを受け取り、オプションの配列を返す必要があります。連想配列を返す場合は、選択したオプションのキーが返されます。それ以外の場合は、代わりに値が返されます。

値を返す配列をフィルタリングする場合は、配列が結合しないように `array_values` 関数または `values` Collection メソッドを使用する必要があります。

```php
$names = collect(['Taylor', 'Abigail']);

$selected = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

プレースホルダー テキストと情報ヒントを含めることもできます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を指定してこれをカスタマイズできます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-required"></a>
#### 値の要求

デフォルトでは、ユーザーは 0 個以上のオプションを選択できます。代わりに、`required` 引数を渡して 1 つ以上のオプションを適用できます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

検証メッセージをカスタマイズしたい場合は、`required` 引数に文字列を指定することもできます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>
#### 追加の検証

追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::whereLike('name', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', and ').' have opted out.';
        }
    }
);
```

`options` クロージャが連想配列を返す場合、クロージャは選択されたキーを受け取ります。それ以外の場合は、選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="pause"></a>
### 一時停止

`pause` 関数を使用すると、ユーザーに情報テキストを表示し、Enter / Return キーを押して続行の確認を待つことができます。

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 検証前の入力の変換 (Transforming Input Before Validation)

場合によっては、検証が行われる前にプロンプ​​ト入力を変換したい場合があります。たとえば、提供された文字列から空白を削除したい場合があります。これを実現するために、プロンプト関数の多くは、クロージャーを受け入れる `transform` 引数を提供します。

```php
$name = text(
    label: 'What is your name?',
    transform: fn (string $value) => trim($value),
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

<a name="forms"></a>
## フォーム (Forms)

多くの場合、追加のアクションを実行する前に情報を収集するために、複数のプロンプトが順番に表示されます。 `form` 関数を使用して、ユーザーが完了するためのグループ化されたプロンプトのセットを作成できます。

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` メソッドは、フォームのプロンプトからのすべての応答を含む数値インデックス付き配列を返します。ただし、`name` 引数を介して各プロンプトに名前を指定できます。名前を指定すると、その名前を介して、指定されたプロンプトの応答にアクセスできます。

```php
use App\Models\User;
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->password(
        label: 'What is your password?',
        validate: ['password' => 'min:8'],
        name: 'password'
    )
    ->confirm('Do you accept the terms?')
    ->submit();

User::create([
    'name' => $responses['name'],
    'password' => $responses['password'],
]);
```

`form` 関数を使用する主な利点は、ユーザーが `CTRL + U` を使用してフォーム内の前のプロンプトに戻ることができることです。これにより、ユーザーはフォーム全体をキャンセルして再起動することなく、間違いを修正したり選択内容を変更したりすることができます。

フォーム内のプロンプトをより詳細に制御する必要がある場合は、プロンプト関数の 1 つを直接呼び出す代わりに、`add` メソッドを呼び出すことができます。 `add` メソッドには、ユーザーが提供した以前のすべての応答が渡されます。

```php
use function Laravel\Prompts\form;
use function Laravel\Prompts\outro;
use function Laravel\Prompts\text;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->add(function ($responses) {
        return text("How old are you, {$responses['name']}?");
    }, name: 'age')
    ->submit();

outro("Your name is {$responses['name']} and you are {$responses['age']} years old.");
```

<a name="informational-messages"></a>
## 情報メッセージ (Informational Messages)

`note`、`info`、`warning`、`error`、および `alert` 関数は、情報メッセージを表示するために使用できます。

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## テーブル (Tables)

`table` 関数を使用すると、複数の行と列のデータを簡単に表示できます。テーブルの列名とデータを指定するだけです。

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## スピン (Spin)

`spin` 関数は、指定されたコールバックの実行中に、オプションのメッセージとともにスピナーを表示します。これは進行中のプロセスを示す役割を果たし、完了時にコールバックの結果を返します。

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> `spin` 関数では、スピナーをアニメーション化するために [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 拡張機能が必要です。この拡張機能が利用できない場合は、代わりに静的バージョンのスピナーが表示されます。

<a name="progress"></a>
## プログレスバー (Progress Bars)

長時間実行されるタスクの場合は、タスクの完了度をユーザーに知らせる進行状況バーを表示すると便利です。 `progress` 関数を使用すると、Laravel は進行状況バーを表示し、指定された反復可能な値を超えて反復ごとに進行状況を進めます。

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 関数はマップ関数のように動作し、コールバックの各反復の戻り値を含む配列を返します。

コールバックは `Laravel\Prompts\Progress` インスタンスも受け入れることができるため、各反復でラベルとヒントを変更できます。

```php
$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: function ($user, $progress) {
        $progress
            ->label("Updating {$user->name}")
            ->hint("Created on {$user->created_at}");

        return $this->performTask($user);
    },
    hint: 'This may take some time.'
);
```

場合によっては、進行状況バーの進み方を手動で制御する必要がある場合があります。まず、プロセスが反復処理される合計ステップ数を定義します。次に、各項目を処理した後、`advance` メソッドを使用して進行状況バーを進めます。

```php
$progress = progress(label: 'Updating users', steps: 10);

$users = User::all();

$progress->start();

foreach ($users as $user) {
    $this->performTask($user);

    $progress->advance();
}

$progress->finish();
```

<a name="clear"></a>
## ターミナルのクリア (Clearing the Terminal)

`clear` 関数は、ユーザーの端末をクリアするために使用できます。

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 端末に関する考慮事項 (Terminal Considerations)

<a name="terminal-width"></a>
#### 端子幅

ラベル、オプション、または検証メッセージの長さがユーザーの端末の「列」数を超える場合、収まるように自動的に切り詰められます。ユーザーが幅の狭い端末を使用している可能性がある場合は、これらの文字列の長さを最小限に抑えることを検討してください。通常、80 文字の端末をサポートするための安全な最大長は 74 文字です。

<a name="terminal-height"></a>
#### 端子高さ

`scroll` 引数を受け入れるプロンプトの場合、構成された値は、検証メッセージ用のスペースを含め、ユーザーの端末の高さに合わせて自動的に縮小されます。

<a name="fallbacks"></a>
## サポートされていない環境とフォールバック (Unsupported Environments and Fallbacks)

Laravel プロンプトは、WSL を使用して macOS、Linux、および Windows をサポートします。 PHP の Windows バージョンの制限のため、現在、WSL 以外の Windows 上で Laravel プロンプトを使用することはできません。

このため、Laravel プロンプトは、[Symfony コンソールの質問ヘルパ](https://symfony.com/doc/current/components/console/helpers/questionhelper.html) などの代替実装へのフォールバックをサポートしています。

> [!NOTE]
> Laravel フレームワークで Laravel プロンプトを使用する場合、各プロンプトのフォールバックが設定されており、サポートされていない環境では自動的に有効になります。

<a name="fallback-conditions"></a>
#### フォールバック条件

Laravel を使用していない場合、またはフォールバック動作を使用するときにカスタマイズする必要がある場合は、`Prompt` クラスの `fallbackWhen` 静的メソッドにブール値を渡すことができます。

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### フォールバック動作

Laravel を使用していない場合、またはフォールバック動作をカスタマイズする必要がある場合は、各プロンプト クラスの `fallbackUsing` 静的メソッドにクロージャーを渡すことができます。

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(
                    is_string($prompt->required) ? $prompt->required : 'Required.'
                );
            }

            if ($prompt->validate) {
                $error = ($prompt->validate)($answer ?? '');

                if ($error) {
                    throw new \RuntimeException($error);
                }
            }

            return $answer;
        });

    return (new SymfonyStyle($input, $output))
        ->askQuestion($question);
});
```

フォールバックは、プロンプト クラスごとに個別に構成する必要があります。クロージャはプロンプト クラスのインスタンスを受け取り、プロンプトの適切なタイプを返さなければなりません。

<a name="testing"></a>
## テスト (Testing)

Laravel には、コマンドが予期したプロンプト メッセージを表示するかどうかをテストするためのさまざまな方法が用意されています。

```php tab=Pest
test('report generation', function () {
    $this->artisan('report:generate')
        ->expectsPromptsInfo('Welcome to the application!')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsAlert('Important notice!')
        ->expectsPromptsIntro('Starting process...')
        ->expectsPromptsOutro('Process completed!')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', 'taylor@example.com'],
                ['Jason Beggs', 'jason@example.com'],
            ]
        )
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
public function test_report_generation(): void
{
    $this->artisan('report:generate')
        ->expectsPromptsInfo('Welcome to the application!')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsAlert('Important notice!')
        ->expectsPromptsIntro('Starting process...')
        ->expectsPromptsOutro('Process completed!')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', 'taylor@example.com'],
                ['Jason Beggs', 'jason@example.com'],
            ]
        )
        ->assertExitCode(0);
}
```

