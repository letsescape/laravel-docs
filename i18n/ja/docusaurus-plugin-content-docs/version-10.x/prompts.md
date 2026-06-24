<!-- # Prompts -->
# Prompts

- [Introduction](#introduction)
- [Installation](#installation)
- [Available Prompts](#available-prompts)
    - [Text](#text)
    - [Password](#password)
    - [Confirm](#confirm)
    - [Select](#select)
    - [Multi-select](#multiselect)
    - [Suggest](#suggest)
    - [Search](#search)
    - [Multi-search](#multisearch)
    - [Pause](#pause)
- [Informational Messages](#informational-messages)
- [Tables](#tables)
- [Spin](#spin)
- [Progress Bar](#progress)
- [Terminal Considerations](#terminal-considerations)
- [Unsupported Environments and Fallbacks](#fallbacks)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Prompts](https://github.com/laravel/prompts) is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation. -->
[Laravel Prompts](https://github.com/laravel/prompts) は、プレースホルダー テキストや検証などのブラウザーのような機能を備えた、美しくユーザーフレンドリーなフォームをコマンドライン アプリケーションに追加するための PHP パッケージです。

<!-- <img src="https://laravel.com/img/docs/prompts-example.png"/> -->
<img src="https://laravel.com/img/docs/prompts-example.png"/>

<!-- Laravel Prompts is perfect for accepting user input in your [Artisan console commands](/docs/10.x/artisan#writing-commands), but it may also be used in any command-line PHP project. -->
Laravel プロンプトは、[Artisan console commands](/docs/10.x/artisan#writing-commands) でユーザー入力を受け入れるのに最適ですが、コマンドライン PHP プロジェクトでも使用できます。

> [!NOTE]
> Laravel プロンプトは、WSL を使用して macOS、Linux、および Windows をサポートします。詳細については、[unsupported environments & fallbacks](#fallbacks) のドキュメントを参照してください。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Laravel Prompts is already included with the latest release of Laravel. -->
Laravel Prompts は、Laravel の最新リリースにすでに含まれています。

<!-- Laravel Prompts may also be installed in your other PHP projects by using the Composer package manager: -->
Laravel プロンプトは、Composer パッケージ マネージャーを使用して他の PHP プロジェクトにインストールすることもできます。

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
<!-- ## Available Prompts -->
## Available Prompts

<a name="text"></a>
<!-- ### Text -->
### Text

<!-- The `text` function will prompt the user with the given question, accept their input, and then return it: -->
`text` 関数は、ユーザーに指定された質問を表示し、入力を受け入れて、それを返します。

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
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
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
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

<!-- The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes. -->
クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="password"></a>
<!-- ### Password -->
### Password

<!-- The `password` function is similar to the `text` function, but the user's input will be masked as they type in the console. This is useful when asking for sensitive information such as passwords: -->
`password` 関数は `text` 関数に似ていますが、ユーザーの入力はコンソールに入力するときにマスクされます。これは、パスワードなどの機密情報を要求する場合に役立ちます。

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

<!-- You may also include placeholder text and an informational hint: -->
プレースホルダー テキストと情報ヒントを含めることもできます。

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
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

<!-- The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes. -->
クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="confirm"></a>
<!-- ### Confirm -->
### Confirm

<!-- If you need to ask the user for a "yes or no" confirmation, you may use the `confirm` function. Users may use the arrow keys or press `y` or `n` to select their response. This function will return either `true` or `false`. -->
ユーザーに「はいまたはいいえ」の確認を求める必要がある場合は、`confirm` 関数を使用できます。ユーザーは矢印キーを使用するか、`y` または `n` を押して応答を選択できます。この関数は、`true` または `false` を返します。

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

<!-- You may also include a default value, customized wording for the "Yes" and "No" labels, and an informational hint: -->
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
<!-- #### Requiring "Yes" -->
#### Requiring "Yes"

<!-- If necessary, you may require your users to select "Yes" by passing the `required` argument: -->
必要に応じて、`required` 引数を渡して、ユーザーに「はい」を選択するよう要求することもできます。

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
<!-- ### Select -->
### Select

<!-- If you need the user to select from a predefined set of choices, you may use the `select` function: -->
ユーザーに事前定義された一連の選択肢から選択する必要がある場合は、`select` 関数を使用できます。

```php
use function Laravel\Prompts\select;

$role = select(
    'What role should the user have?',
    ['Member', 'Contributor', 'Owner'],
);
```

<!-- You may also specify the default choice and an informational hint: -->
デフォルトの選択と情報ヒントを指定することもできます。

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

<!-- You may also pass an associative array to the `options` argument to have the selected key returned instead of its value: -->
連想配列を `options` 引数に渡して、値の代わりに選択したキーを返すようにすることもできます。

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner'
    ],
    default: 'owner'
);
```

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument: -->
リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を渡すことでこれをカスタマイズできます。

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
<!-- #### Validation -->
#### Validation

<!-- Unlike other prompt functions, the `select` function doesn't accept the `required` argument because it is not possible to select nothing. However, you may pass a closure to the `validate` argument if you need to present an option but prevent it from being selected: -->
他のプロンプト関数とは異なり、`select` 関数は何も選択できないため、`required` 引数を受け入れません。ただし、オプションを提示する必要があるが選択されないようにする場合は、`validate` 引数にクロージャーを渡すことができます。

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner'
    ],
    validate: fn (string $value) =>
        $value === 'owner' && User::where('role', 'owner')->exists()
            ? 'An owner already exists.'
            : null
);
```

<!-- If the `options` argument is an associative array, then the closure will receive the selected key, otherwise it will receive the selected value. The closure may return an error message, or `null` if the validation passes. -->
`options` 引数が連想配列の場合、クロージャは選択されたキーを受け取り、それ以外の場合は選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="multiselect"></a>
<!-- ### Multi-select -->
### Multi-select

<!-- If you need to the user to be able to select multiple options, you may use the `multiselect` function: -->
ユーザーが複数のオプションを選択できるようにする必要がある場合は、`multiselect` 関数を使用できます。

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    'What permissions should be assigned?',
    ['Read', 'Create', 'Update', 'Delete']
);
```

<!-- You may also specify default choices and an informational hint: -->
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

<!-- You may also pass an associative array to the `options` argument to return the selected options' keys instead of their values: -->
連想配列を `options` 引数に渡して、選択したオプションの値の代わりにキーを返すこともできます。

```
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete'
    ],
    default: ['read', 'create']
);
```

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument: -->
リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を渡すことでこれをカスタマイズできます。

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
<!-- #### Requiring a Value -->
#### Requiring a Value

<!-- By default, the user may select zero or more options. You may pass the `required` argument to enforce one or more options instead: -->
デフォルトでは、ユーザーは 0 個以上のオプションを選択できます。代わりに、`required` 引数を渡して 1 つ以上のオプションを適用できます。

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true,
);
```

<!-- If you would like to customize the validation message, you may provide a string to the `required` argument: -->
検証メッセージをカスタマイズしたい場合は、`required` 引数に文字列を指定できます。

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category',
);
```

<a name="multiselect-validation"></a>
<!-- #### Validation -->
#### Validation

<!-- You may pass a closure to the `validate` argument if you need to present an option but prevent it from being selected: -->
オプションを提示する必要があるが、それが選択されないようにする場合は、`validate` 引数にクロージャーを渡すことができます。

```
$permissions = multiselect(
    label: 'What permissions should the user have?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete'
    ],
    validate: fn (array $values) => ! in_array('read', $values)
        ? 'All users require the read permission.'
        : null
);
```

<!-- If the `options` argument is an associative array then the closure will receive the selected keys, otherwise it will receive the selected values. The closure may return an error message, or `null` if the validation passes. -->
`options` 引数が連想配列の場合、クロージャは選択されたキーを受け取り、それ以外の場合は選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="suggest"></a>
<!-- ### Suggest -->
### Suggest

<!-- The `suggest` function can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`suggest` 関数を使用すると、可能な選択肢のオートコンプリートを提供できます。ユーザーは、オートコンプリートのヒントに関係なく、任意の回答を入力できます。

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `suggest` function. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far and return an array of options for auto-completion: -->
あるいは、`suggest` 関数の 2 番目の引数としてクロージャを渡すこともできます。クロージャは、ユーザーが入力文字を入力するたびに呼び出されます。クロージャは、これまでのユーザーの入力を含む文字列パラメータを受け入れ、オートコンプリートのオプションの配列を返す必要があります。

```php
$name = suggest(
    'What is your name?',
    fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
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
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
値を入力する必要がある場合は、`required` 引数を渡すことができます。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
検証メッセージをカスタマイズしたい場合は、文字列を渡すこともできます。

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
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

<!-- The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes. -->
クロージャは入力された値を受け取り、エラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="search"></a>
<!-- ### Search -->
### Search

<!-- If you have a lot of options for the user to select from, the `search` function allows the user to type a search query to filter the results before using the arrow keys to select an option: -->
ユーザーが選択できるオプションが多数ある場合、`search` 関数を使用すると、ユーザーは矢印キーを使用してオプションを選択する前に、検索クエリを入力して結果をフィルタリングできます。

```php
use function Laravel\Prompts\search;

$id = search(
    'Search for the user that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

<!-- The closure will receive the text that has been typed by the user so far and must return an array of options. If you return an associative array then the selected option's key will be returned, otherwise its value will be returned instead. -->
クロージャは、ユーザーがこれまでに入力したテキストを受け取り、オプションの配列を返す必要があります。連想配列を返す場合は、選択したオプションのキーが返され、それ以外の場合は、代わりにその値が返されます。

<!-- You may also include placeholder text and an informational hint: -->
プレースホルダー テキストと情報ヒントを含めることもできます。

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument: -->
リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を渡すことでこれをカスタマイズできます。

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-validation"></a>
<!-- #### Validation -->
#### Validation

<!-- If you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return 'This user has opted-out of receiving mail.';
        }
    }
);
```

<!-- If the `options` closure returns an associative array, then the closure will receive the selected key, otherwise, it will receive the selected value. The closure may return an error message, or `null` if the validation passes. -->
`options` クロージャが連想配列を返す場合、クロージャは選択されたキーを受け取り、そうでない場合は、選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="multisearch"></a>
<!-- ### Multi-search -->
### Multi-search

<!-- If you have a lot of searchable options and need the user to be able to select multiple items, the `multisearch` function allows the user to type a search query to filter the results before using the arrow keys and space-bar to select options: -->
検索可能なオプションが多数あり、ユーザーが複数の項目を選択できるようにする必要がある場合、`multisearch` 関数を使用すると、ユーザーは矢印キーとスペースバーを使用してオプションを選択する前に、検索クエリを入力して結果をフィルタリングできます。

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

<!-- The closure will receive the text that has been typed by the user so far and must return an array of options. If you return an associative array then the selected options' keys will be returned; otherwise, their values will be returned instead. -->
クロージャは、ユーザーがこれまでに入力したテキストを受け取り、オプションの配列を返す必要があります。連想配列を返す場合は、選択したオプションのキーが返されます。それ以外の場合は、代わりに値が返されます。

<!-- You may also include placeholder text and an informational hint: -->
プレースホルダー テキストと情報ヒントを含めることもできます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by providing the `scroll` argument: -->
リストのスクロールが始まる前に、最大 5 つのオプションが表示されます。 `scroll` 引数を指定してこれをカスタマイズできます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-required"></a>
<!-- #### Requiring a Value -->
#### Requiring a Value

<!-- By default, the user may select zero or more options. You may pass the `required` argument to enforce one or more options instead: -->
デフォルトでは、ユーザーは 0 個以上のオプションを選択できます。代わりに、`required` 引数を渡して 1 つ以上のオプションを適用できます。

```php
$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true,
);
```

<!-- If you would like to customize the validation message, you may also provide a string to the `required` argument: -->
検証メッセージをカスタマイズしたい場合は、`required` 引数に文字列を指定することもできます。

```php
$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>
<!-- #### Validation -->
#### Validation

<!-- If you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
追加の検証ロジックを実行したい場合は、`validate` 引数にクロージャを渡すことができます。

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::where('name', 'like', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', and ').' have opted out.';
        }
    }
);
```

<!-- If the `options` closure returns an associative array, then the closure will receive the selected keys; otherwise, it will receive the selected values. The closure may return an error message, or `null` if the validation passes. -->
`options` クロージャが連想配列を返す場合、クロージャは選択されたキーを受け取ります。それ以外の場合は、選択された値を受け取ります。クロージャはエラー メッセージを返すか、検証に合格した場合は `null` を返す場合があります。

<a name="pause"></a>
<!-- ### Pause -->
### Pause

<!-- The `pause` function may be used to display informational text to the user and wait for them to confirm their desire to proceed by pressing the Enter / Return key: -->
`pause` 関数を使用すると、ユーザーに情報テキストを表示し、Enter / Return キーを押して続行の確認を待つことができます。

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="informational-messages"></a>
<!-- ## Informational Messages -->
## Informational Messages

<!-- The `note`, `info`, `warning`, `error`, and `alert` functions may be used to display informational messages: -->
`note`、`info`、`warning`、`error`、および `alert` 関数は、情報メッセージを表示するために使用できます。

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<!-- The `table` function makes it easy to display multiple rows and columns of data. All you need to do is provide the column names and the data for the table: -->
`table` 関数を使用すると、複数の行と列のデータを簡単に表示できます。テーブルの列名とデータを指定するだけです。

```php
use function Laravel\Prompts\table;

table(
    ['Name', 'Email'],
    User::all(['name', 'email'])
);
```

<a name="spin"></a>
<!-- ## Spin -->
## Spin

<!-- The `spin` function displays a spinner along with an optional message while executing a specified callback. It serves to indicate ongoing processes and returns the callback's results upon completion: -->
`spin` 関数は、指定されたコールバックの実行中に、オプションのメッセージとともにスピナーを表示します。これは進行中のプロセスを示す役割を果たし、完了時にコールバックの結果を返します。

```php
use function Laravel\Prompts\spin;

$response = spin(
    fn () => Http::get('http://example.com'),
    'Fetching response...'
);
```

> [!WARNING]
> `spin` 関数でスピナーをアニメーション化するには、`pcntl` PHP 拡張機能が必要です。この拡張機能が利用できない場合は、代わりに静的バージョンのスピナーが表示されます。

<a name="progress"></a>
<!-- ## Progress Bars -->
## Progress Bars

<!-- For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `progress` function, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value: -->
長時間実行されるタスクの場合は、タスクの完了度をユーザーに知らせる進行状況バーを表示すると便利です。 `progress` 関数を使用すると、Laravel は進行状況バーを表示し、指定された反復可能な値を超えて反復ごとに進行状況を進めます。

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user),
);
```

<!-- The `progress` function acts like a map function and will return an array containing the return value of each iteration of your callback. -->
`progress` 関数はマップ関数のように動作し、コールバックの各反復の戻り値を含む配列を返します。

<!-- The callback may also accept the `\Laravel\Prompts\Progress` instance, allowing you to modify the label and hint on each iteration: -->
コールバックは `\Laravel\Prompts\Progress` インスタンスも受け入れることができるため、各反復でラベルとヒントを変更できます。

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
    hint: 'This may take some time.',
);
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar via the `advance` method after processing each item: -->
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

<a name="terminal-considerations"></a>
<!-- ## Terminal Considerations -->
## Terminal Considerations

<a name="terminal-width"></a>
<!-- #### Terminal Width -->
#### Terminal Width

<!-- If the length of any label, option, or validation message exceeds the number of "columns" in the user's terminal, it will be automatically truncated to fit. Consider minimizing the length of these strings if your users may be using narrower terminals. A typically safe maximum length is 74 characters to support an 80-character terminal. -->
ラベル、オプション、または検証メッセージの長さがユーザーの端末の「列」数を超える場合、収まるように自動的に切り詰められます。ユーザーが幅の狭い端末を使用している可能性がある場合は、これらの文字列の長さを最小限に抑えることを検討してください。通常、80 文字の端末をサポートするための安全な最大長は 74 文字です。

<a name="terminal-height"></a>
<!-- #### Terminal Height -->
#### Terminal Height

<!-- For any prompts that accept the `scroll` argument, the configured value will automatically be reduced to fit the height of the user's terminal, including space for a validation message. -->
`scroll` 引数を受け入れるプロンプトの場合、構成された値は、検証メッセージ用のスペースを含め、ユーザーの端末の高さに合わせて自動的に縮小されます。

<a name="fallbacks"></a>
<!-- ## Unsupported Environments and Fallbacks -->
## Unsupported Environments and Fallbacks

<!-- Laravel Prompts supports macOS, Linux, and Windows with WSL. Due to limitations in the Windows version of PHP, it is not currently possible to use Laravel Prompts on Windows outside of WSL. -->
Laravel プロンプトは、WSL を使用して macOS、Linux、および Windows をサポートします。 PHP の Windows バージョンの制限のため、現在、WSL 以外の Windows 上で Laravel プロンプトを使用することはできません。

<!-- For this reason, Laravel Prompts supports falling back to an alternative implementation such as the [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html). -->
このため、Laravel プロンプトは、[Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html) などの代替実装へのフォールバックをサポートしています。

> [!NOTE]
> Laravel フレームワークで Laravel プロンプトを使用する場合、各プロンプトのフォールバックが設定されており、サポートされていない環境では自動的に有効になります。

<a name="fallback-conditions"></a>
<!-- #### Fallback Conditions -->
#### Fallback Conditions

<!-- If you are not using Laravel or need to customize when the fallback behavior is used, you may pass a boolean to the `fallbackWhen` static method on the `Prompt` class: -->
Laravel を使用していない場合、またはフォールバック動作を使用するときにカスタマイズする必要がある場合は、`Prompt` クラスの `fallbackWhen` 静的メソッドにブール値を渡すことができます。

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
<!-- #### Fallback Behavior -->
#### Fallback Behavior

<!-- If you are not using Laravel or need to customize the fallback behavior, you may pass a closure to the `fallbackUsing` static method on each prompt class: -->
Laravel を使用していない場合、またはフォールバック動作をカスタマイズする必要がある場合は、各プロンプト クラスの `fallbackUsing` 静的メソッドにクロージャーを渡すことができます。

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(is_string($prompt->required) ? $prompt->required : 'Required.');
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

<!-- Fallbacks must be configured individually for each prompt class. The closure will receive an instance of the prompt class and must return an appropriate type for the prompt. -->
フォールバックは、プロンプト クラスごとに個別に構成する必要があります。クロージャはプロンプト クラスのインスタンスを受け取り、プロンプトの適切なタイプを返さなければなりません。

