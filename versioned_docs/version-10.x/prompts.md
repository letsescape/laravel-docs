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
[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에서 아름답고 사용자 친화적인 폼을 추가할 수 있도록 해주는 PHP 패키지입니다. 이 패키지는 플레이스홀더 텍스트 및 유효성 검증과 같은 브라우저급 기능들을 제공합니다.

<!-- <img src="https://laravel.com/img/docs/prompts-example.png"/> -->
<img src="https://laravel.com/img/docs/prompts-example.png" />

<!-- Laravel Prompts is perfect for accepting user input in your [Artisan console commands](/docs/10.x/artisan#writing-commands), but it may also be used in any command-line PHP project. -->
Laravel Prompts는 [Artisan console commands](/docs/10.x/artisan#writing-commands)에서 사용자 입력을 받을 때 특히 적합하지만, 어떤 커맨드라인 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, 그리고 WSL이 설치된 Windows에서 지원됩니다. 자세한 내용은 [unsupported environments & fallbacks](#fallbacks) 문서를 참고하시기 바랍니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Laravel Prompts is already included with the latest release of Laravel. -->
Laravel Prompts는 최신 Laravel 릴리스에 기본 포함되어 있습니다.

<!-- Laravel Prompts may also be installed in your other PHP projects by using the Composer package manager: -->
또한, Composer 패키지 관리자를 사용하여 다른 PHP 프로젝트에도 설치할 수 있습니다:

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
`text` 함수는 사용자가 질문에 답할 수 있도록 입력을 요청하고, 입력값을 반환합니다.

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더 텍스트, 기본값, 안내 힌트를 함께 제공할 수도 있습니다.

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
값 입력이 필수라면 `required` 인수를 넘기면 됩니다.

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 메시지를 변경하고 싶다면 문자열로 직접 지정할 수도 있습니다.

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
추가적인 검증 로직이 필요하다면, `validate` 인수에 클로저를 전달할 수 있습니다.

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
이 클로저는 입력값을 받아서, 유효성 검증에 실패한 경우 에러 메시지를 반환하거나, 검증에 통과하면 `null`을 반환합니다.

<a name="password"></a>
<!-- ### Password -->
### Password

<!-- The `password` function is similar to the `text` function, but the user's input will be masked as they type in the console. This is useful when asking for sensitive information such as passwords: -->
`password` 함수는 `text` 함수와 비슷하지만, 사용자의 입력이 콘솔에서 가려져서 표시됩니다. 주로 비밀번호 등 민감한 정보를 입력받을 때 사용됩니다.

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

<!-- You may also include placeholder text and an informational hint: -->
플레이스홀더 텍스트와 안내 힌트도 함께 추가할 수 있습니다.

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
값 입력이 필수라면 `required` 인수를 넘기면 됩니다.

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
검증 메시지를 커스터마이즈하고 싶다면 문자열로 지정할 수도 있습니다.

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
패스워드에 대해 추가적인 유효성 검증이 필요하다면, `validate` 인수에 클로저를 전달할 수 있습니다.

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
이 클로저는 입력값을 받아서, 유효성 규칙에 맞지 않으면 에러 메시지를, 맞으면 `null`을 반환합니다.

<a name="confirm"></a>
<!-- ### Confirm -->
### Confirm

<!-- If you need to ask the user for a "yes or no" confirmation, you may use the `confirm` function. Users may use the arrow keys or press `y` or `n` to select their response. This function will return either `true` or `false`. -->
사용자에게 "예/아니요"로 답하는 확인을 요청해야 한다면, `confirm` 함수를 사용할 수 있습니다. 화살표 키나 `y`, `n` 키로 선택할 수 있으며, `true` 또는 `false` 값을 반환합니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

<!-- You may also include a default value, customized wording for the "Yes" and "No" labels, and an informational hint: -->
기본값, "예/아니요" 버튼 문구, 안내 힌트도 자유롭게 지정할 수 있습니다.

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
필요하다면 `required` 인수를 사용해 사용자가 반드시 "예"를 선택해야만 통과하도록 만들 수 있습니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
맞춤 검증 메시지를 사용하려면 문자열로 지정하면 됩니다.

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
사용자가 미리 정해진 선택지 중에서 하나를 고르게 하려면, `select` 함수를 사용할 수 있습니다.

```php
use function Laravel\Prompts\select;

$role = select(
    'What role should the user have?',
    ['Member', 'Contributor', 'Owner'],
);
```

<!-- You may also specify the default choice and an informational hint: -->
기본 선택값과 안내 힌트도 지정할 수 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

<!-- You may also pass an associative array to the `options` argument to have the selected key returned instead of its value: -->
선택지의 키를 반환받고 싶다면, `options` 인수에 연관 배열을 전달할 수 있습니다.

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
최대 5개의 선택지가 한 번에 보여지며, 그 이상이면 스크롤 목록으로 나타나게 됩니다. `scroll` 인수로 한 번에 보여지는 항목 수를 조정할 수 있습니다.

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
다른 프롬프트 함수들과 달리, `select` 함수는 아무 것도 선택하지 않는 상황이 발생할 수 없으므로 `required` 인수를 지원하지 않습니다. 하지만, 선택지 중 일부를 선택 금지해야 할 경우 `validate`에 클로저를 넘겨 조건을 지정할 수 있습니다.

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
`options` 인수가 연관 배열이면 선택한 값의 키가, 그냥 배열이면 값 자체가 클로저에 전달됩니다. 클로저는 에러 메시지(문자열)나, 검증이 통과하면 `null`을 반환해야 합니다.

<a name="multiselect"></a>
<!-- ### Multi-select -->
### Multi-select

<!-- If you need to the user to be able to select multiple options, you may use the `multiselect` function: -->
사용자가 여러 항목을 한 번에 선택할 수 있게 하려면, `multiselect` 함수를 사용합니다.

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    'What permissions should be assigned?',
    ['Read', 'Create', 'Update', 'Delete']
);
```

<!-- You may also specify default choices and an informational hint: -->
기본 선택값 및 안내 힌트도 지정할 수 있습니다.

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
선택된 값의 키만 받고 싶다면, `options` 인수에 연관 배열을 사용하면 됩니다.

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
선택지는 기본적으로 5개까지만 한 번에 보여지며, `scroll` 인수로 개수를 바꿀 수 있습니다.

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
기본적으로 사용자는 아무 옵션도 선택하지 않거나 여러 개를 선택할 수 있습니다. 하지만, 반드시 하나 이상 선택하도록 하려면 `required` 인수를 사용합니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true,
);
```

<!-- If you would like to customize the validation message, you may provide a string to the `required` argument: -->
검증 메시지를 직접 지정하려면 `required` 인수에 문자열을 전달하세요.

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
특정 조건에서 선택을 제한하거나 검증이 필요하다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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
`options` 인수에 연관 배열을 전달하면 선택된 키들의 배열이, 그냥 배열이면 값들의 배열이 클로저에 전달됩니다. 이 클로저는 에러 메시지(문자열)나 검증이 통과되면 `null`을 반환해야 합니다.

<a name="suggest"></a>
<!-- ### Suggest -->
### Suggest

<!-- The `suggest` function can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`suggest` 함수는 사용자가 입력할 때 자동 완성(추천) 옵션을 제공할 수 있습니다. 사용자는 제안된 옵션과 상관없이 자유롭게 값을 입력할 수 있습니다.

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `suggest` function. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far and return an array of options for auto-completion: -->
또는 `suggest` 함수의 두 번째 인수로 클로저를 전달할 수도 있습니다. 이 클로저는 사용자가 문자를 입력할 때마다 호출됩니다. 클로저는 사용자가 지금까지 입력한 문자열을 파라미터로 받아 자동 완성 옵션 배열을 반환해야 합니다.

```php
$name = suggest(
    'What is your name?',
    fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더, 기본값, 안내 힌트도 추가할 수 있습니다.

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
입력이 필수라면 `required` 인수를 사용합니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
검증 메시지를 직접 지정할 수도 있습니다.

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
추가적인 유효성 검증이 필요하다면 `validate` 인수에 클로저를 전달하세요.

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
이 클로저는 입력값을 받아서, 검증에 실패하면 오류 메시지를, 통과하면 `null`을 반환합니다.

<a name="search"></a>
<!-- ### Search -->
### Search

<!-- If you have a lot of options for the user to select from, the `search` function allows the user to type a search query to filter the results before using the arrow keys to select an option: -->
선택 옵션이 많을 경우, `search` 함수를 사용하면 사용자가 검색어를 입력해서 결과를 필터링한 후, 화살표 키로 선택할 수 있습니다.

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
클로저는 사용자가 현재까지 입력한 텍스트를 받아, 추천할 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 키가 값으로, 일반 배열을 반환하면 값이 결과로 반환됩니다.

<!-- You may also include placeholder text and an informational hint: -->
플레이스홀더와 안내 힌트를 추가할 수도 있습니다.

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
옵션은 최대 5개까지 한 번에 보여지며, `scroll` 인수로 더 많은 결과가 보이도록 설정할 수 있습니다.

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
추가적으로 유효성 검증을 적용하고 싶을 때는 `validate`에 클로저를 넣을 수 있습니다.

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
`options` 클로저가 연관 배열을 반환하면 선택된 키가, 일반 배열이면 값이 클로저에 전달됩니다. 클로저는 에러 메시지나 통과할 경우 `null`을 반환합니다.

<a name="multisearch"></a>
<!-- ### Multi-search -->
### Multi-search

<!-- If you have a lot of searchable options and need the user to be able to select multiple items, the `multisearch` function allows the user to type a search query to filter the results before using the arrow keys and space-bar to select options: -->
많은 옵션 중 여러 항목을 동시에 선택해야 한다면 `multisearch` 함수를 사용할 수 있습니다. 이 함수는 사용자가 검색어로 옵션을 필터링한 뒤, 화살표 키와 스페이스바로 여러 개를 선택할 수 있게 해줍니다.

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
클로저는 입력된 검색어를 받아 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 키 목록이, 일반 배열을 반환하면 값들의 배열이 결과로 반환됩니다.

<!-- You may also include placeholder text and an informational hint: -->
플레이스홀더와 안내 힌트도 지정 가능합니다.

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
화면에 한 번에 보여지는 옵션 수는 5개까지이며, `scroll` 인수로 개수를 조정할 수 있습니다.

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
기본적으로 사용자는 아무 옵션도 선택하지 않거나 여러 개를 선택할 수 있습니다. 하지만 반드시 하나 이상 선택하도록 요구하려면 `required` 인수를 사용하면 됩니다.

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
검증 메시지를 직접 지정하려면 `required` 인수에 문자열을 전달하면 됩니다.

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
추가적인 유효성 검증이 필요하다면 `validate`에 클로저를 넣어 원하는 조건을 구현할 수 있습니다.

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
`options` 클로저가 연관 배열을 반환하면 선택된 키들이, 일반 배열이면 값들이 클로저에 전달됩니다. 클로저는 에러 메시지나 `null`을 반환할 수 있습니다.

<a name="pause"></a>
<!-- ### Pause -->
### Pause

<!-- The `pause` function may be used to display informational text to the user and wait for them to confirm their desire to proceed by pressing the Enter / Return key: -->
`pause` 함수는 사용자가 엔터(Enter) 또는 리턴(Return) 키를 누를 때까지, 안내 메시지와 함께 잠시 멈추도록 할 때 사용할 수 있습니다.

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="informational-messages"></a>
<!-- ## Informational Messages -->
## Informational Messages

<!-- The `note`, `info`, `warning`, `error`, and `alert` functions may be used to display informational messages: -->
`note`, `info`, `warning`, `error`, `alert` 함수들은 다양한 정보 메시지를 출력할 때 사용할 수 있습니다.

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<!-- The `table` function makes it easy to display multiple rows and columns of data. All you need to do is provide the column names and the data for the table: -->
`table` 함수는 여러 행(row)과 열(column)의 데이터를 쉽고 보기 좋게 출력해줍니다. 열 이름과 데이터만 전달하면 됩니다.

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
`spin` 함수는 지정한 콜백이 실행되는 동안, 진행 중임을 나타내는 스피너와 함께, 메시지를 표시해줍니다. 실행이 끝나면 콜백의 결과값을 반환합니다.

```php
use function Laravel\Prompts\spin;

$response = spin(
    fn () => Http::get('http://example.com'),
    'Fetching response...'
);
```

> [!WARNING]
> `spin` 함수에서 애니메이션 스피너를 사용하려면 `pcntl` PHP 확장 모듈이 필요합니다. 만약 이 확장이 없으면, 정적인(움직이지 않는) 스피너가 대신 표시됩니다.

<a name="progress"></a>
<!-- ## Progress Bars -->
## Progress Bars

<!-- For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `progress` function, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value: -->
실행 시간이 긴 작업의 진행 상황을 사용자에게 보여주고 싶을 때는 `progress` 함수를 사용해 진행률 바를 표시할 수 있습니다. 지정한 데이터를 반복(iterate)하면서 각 반복마다 진행도가 올라갑니다.

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user),
);
```

<!-- The `progress` function acts like a map function and will return an array containing the return value of each iteration of your callback. -->
`progress` 함수는 map 함수처럼 동작하며, 각 콜백 반환값이 담긴 배열을 결과로 반환합니다.

<!-- The callback may also accept the `\Laravel\Prompts\Progress` instance, allowing you to modify the label and hint on each iteration: -->
콜백에서 `\Laravel\Prompts\Progress` 인스턴스를 두 번째 인수로 받아, 반복 단계마다 라벨이나 힌트를 바꿀 수도 있습니다.

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
진행률 바를 더 세세하게 직접 제어하려면, 프로세스 전체 반복 횟수(steps)를 지정하고, 각 단계마다 `advance` 메서드로 수동으로 진행도를 올릴 수도 있습니다.

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
라벨, 옵션, 유효성 메시지 등 문자열의 길이가 현재 사용자의 터미널 너비(컬럼 수)를 넘는 경우, 자동으로 잘려서 표시됩니다. 터미널 화면이 좁은 환경을 고려해 74자 이내(80자 터미널 기준)로 짧게 작성하는 것이 안전합니다.

<a name="terminal-height"></a>
<!-- #### Terminal Height -->
#### Terminal Height

<!-- For any prompts that accept the `scroll` argument, the configured value will automatically be reduced to fit the height of the user's terminal, including space for a validation message. -->
`scroll` 인수를 사용할 수 있는 프롬프트는, 설정된 개수가 사용자의 터미널 높이에 맞춰 자동으로 줄어듭니다. 유효성 메시지를 표시할 공간도 함께 고려됩니다.

<a name="fallbacks"></a>
<!-- ## Unsupported Environments and Fallbacks -->
## Unsupported Environments and Fallbacks

<!-- Laravel Prompts supports macOS, Linux, and Windows with WSL. Due to limitations in the Windows version of PHP, it is not currently possible to use Laravel Prompts on Windows outside of WSL. -->
Laravel Prompts는 macOS, Linux, 그리고 WSL 환경의 Windows에서 지원됩니다. 다만, Windows 순정 PHP에서는 기술적 한계로 아직 Laravel Prompts를 직접 사용할 수 없습니다.

<!-- For this reason, Laravel Prompts supports falling back to an alternative implementation such as the [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html). -->
이러한 환경에서는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)와 같은 대체 구현체로 자동 전환됩니다.

> [!NOTE]
> Laravel 프레임워크와 함께 Laravel Prompts를 사용할 때는, 각 프롬프트에 맞는 대체 동작(fallback)이 이미 설정되어 있으며, 지원되지 않는 환경에서 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
<!-- #### Fallback Conditions -->
#### Fallback Conditions

<!-- If you are not using Laravel or need to customize when the fallback behavior is used, you may pass a boolean to the `fallbackWhen` static method on the `Prompt` class: -->
Laravel이 아닌 환경에서, 또는 대체 동작 조건을 직접 지정하고 싶다면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언값을 넘겨 사용합니다.

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
Laravel이 아닌 환경에서 직접 대체 동작을 지정하려면, 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달할 수 있습니다.

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
대체 동작은 각 프롬프트 클래스별로 따로 설정해야 하며, 입력값 및 반환값 타입 역시 각 프롬프트에 맞게 맞춰야 합니다.

