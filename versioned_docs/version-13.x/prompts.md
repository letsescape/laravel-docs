<!-- # Prompts -->
# Prompts

- [Introduction](#introduction)
- [Installation](#installation)
- [Available Prompts](#available-prompts)
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
    - [Autocomplete](#autocomplete)
- [Transforming Input Before Validation](#transforming-input-before-validation)
- [Forms](#forms)
- [Informational Messages](#informational-messages)
- [Tables](#tables)
- [Spin](#spin)
- [Progress Bar](#progress)
- [Task](#task)
- [Stream](#stream)
- [Terminal Title](#terminal-title)
- [Clearing the Terminal](#clear)
- [Terminal Considerations](#terminal-considerations)
- [Unsupported Environments and Fallbacks](#fallbacks)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Prompts](https://github.com/laravel/prompts) is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation. -->
[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 보기 좋고 사용하기 쉬운 폼을 추가할 수 있는 PHP 패키지입니다. 플레이스홀더 텍스트와 유효성 검증처럼 브라우저와 비슷한 기능을 제공합니다.

<!-- <img src="https://laravel.com/img/docs/prompts-example.png"/> -->
<img src="https://laravel.com/img/docs/prompts-example.png"/>

<!-- Laravel Prompts is perfect for accepting user input in your [Artisan console commands](/docs/13.x/artisan#writing-commands), but it may also be used in any command-line PHP project. -->
Laravel Prompts는 [Artisan console commands](/docs/13.x/artisan#writing-commands)에서 사용자 입력을 받을 때 매우 적합하지만, 어떤 명령줄 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, 그리고 WSL을 사용하는 Windows를 지원합니다. 자세한 내용은 [unsupported environments & fallbacks](#fallbacks)에 대한 문서를 참고하십시오.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Laravel Prompts is already included with the latest release of Laravel. -->
Laravel Prompts는 최신 Laravel 릴리스에 이미 포함되어 있습니다.

<!-- Laravel Prompts may also be installed in your other PHP projects by using the Composer package manager: -->
다른 PHP 프로젝트에서도 Composer 패키지 매니저를 사용하여 Laravel Prompts를 설치할 수 있습니다.

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
`text` 함수는 주어진 질문을 사용자에게 표시하고, 입력을 받은 뒤 그 값을 반환합니다.

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더 텍스트, 기본값, 안내용 힌트도 함께 지정할 수 있습니다.

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
값을 반드시 입력해야 한다면 `required` 인수를 전달할 수 있습니다.

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수도 있습니다.

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
마지막으로 추가 유효성 검증 로직을 수행하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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
이 클로저는 입력된 값을 전달받으며, 오류 메시지를 반환하거나 유효성 검증을 통과한 경우 `null`을 반환할 수 있습니다.

<!-- Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument: -->
또는 Laravel의 [validator](/docs/13.x/validation)를 활용할 수도 있습니다. 이를 위해 `validate` 인수에 속성 이름과 원하는 유효성 검증 규칙이 포함된 배열을 전달하십시오.

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
<!-- ### Textarea -->
### Textarea

<!-- The `textarea` function will prompt the user with the given question, accept their input via a multi-line textarea, and then return it: -->
`textarea` 함수는 주어진 질문을 사용자에게 표시하고, 여러 줄을 입력할 수 있는 텍스트 영역으로 입력을 받은 뒤 그 값을 반환합니다.

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더 텍스트, 기본값, 안내용 힌트도 함께 지정할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
값을 반드시 입력해야 한다면 `required` 인수를 전달할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수도 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
마지막으로 추가 유효성 검증 로직을 수행하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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

<!-- The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes. -->
이 클로저는 입력된 값을 전달받으며, 오류 메시지를 반환하거나 유효성 검증을 통과한 경우 `null`을 반환할 수 있습니다.

<!-- Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument: -->
또는 Laravel의 [validator](/docs/13.x/validation)를 활용할 수도 있습니다. 이를 위해 `validate` 인수에 속성 이름과 원하는 유효성 검증 규칙이 포함된 배열을 전달하십시오.

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="number"></a>
<!-- ### Number -->
### Number

<!-- The `number` function will prompt the user with the given question, accept their numeric input, and then return it. The `number` function allows the user to use the up and down arrow keys to manipulate the number: -->
`number` 함수는 주어진 질문을 사용자에게 표시하고, 숫자 입력을 받은 뒤 그 값을 반환합니다. `number` 함수에서는 사용자가 위쪽 및 아래쪽 화살표 키를 사용하여 숫자를 조정할 수 있습니다.

```php
use function Laravel\Prompts\number;

$number = number('How many copies would you like?');
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더 텍스트, 기본값, 안내용 힌트도 함께 지정할 수 있습니다.

```php
$name = number(
    label: 'How many copies would you like?',
    placeholder: '5',
    default: 1,
    hint: 'This will be determine how many copies to create.'
);
```

<a name="number-required"></a>
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
값을 반드시 입력해야 한다면 `required` 인수를 전달할 수 있습니다.

```php
$copies = number(
    label: 'How many copies would you like?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수도 있습니다.

```php
$copies = number(
    label: 'How many copies would you like?',
    required: 'A number of copies is required.'
);
```

<a name="number-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
마지막으로 추가 유효성 검증 로직을 수행하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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

<!-- The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes. -->
이 클로저는 입력된 값을 전달받으며, 오류 메시지를 반환하거나 유효성 검증을 통과한 경우 `null`을 반환할 수 있습니다.

<!-- Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument: -->
또는 Laravel의 [validator](/docs/13.x/validation)를 활용할 수도 있습니다. 이를 위해 `validate` 인수에 속성 이름과 원하는 유효성 검증 규칙이 포함된 배열을 전달하십시오.

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: ['copies' => 'required|integer|min:1|max:100']
);
```

<a name="password"></a>
<!-- ### Password -->
### Password

<!-- The `password` function is similar to the `text` function, but the user's input will be masked as they type in the console. This is useful when asking for sensitive information such as passwords: -->
`password` 함수는 `text` 함수와 비슷하지만, 사용자가 콘솔에 입력하는 동안 입력값이 가려집니다. 비밀번호처럼 민감한 정보를 요청할 때 유용합니다.

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

<!-- You may also include placeholder text and an informational hint: -->
플레이스홀더 텍스트와 안내용 힌트도 함께 지정할 수 있습니다.

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
값을 반드시 입력해야 한다면 `required` 인수를 전달할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수도 있습니다.

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
마지막으로 추가 유효성 검증 로직을 수행하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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
이 클로저는 입력된 값을 전달받으며, 오류 메시지를 반환하거나 유효성 검증을 통과한 경우 `null`을 반환할 수 있습니다.

<!-- Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument: -->
또는 Laravel의 [validator](/docs/13.x/validation)를 활용할 수도 있습니다. 이를 위해 `validate` 인수에 속성 이름과 원하는 유효성 검증 규칙이 포함된 배열을 전달하십시오.

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
<!-- ### Confirm -->
### Confirm

<!-- If you need to ask the user for a "yes or no" confirmation, you may use the `confirm` function. Users may use the arrow keys or press `y` or `n` to select their response. This function will return either `true` or `false`. -->
사용자에게 "yes or no" 확인을 요청해야 한다면 `confirm` 함수를 사용할 수 있습니다. 사용자는 화살표 키를 사용하거나 `y` 또는 `n`을 눌러 응답을 선택할 수 있습니다. 이 함수는 `true` 또는 `false`를 반환합니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

<!-- You may also include a default value, customized wording for the "Yes" and "No" labels, and an informational hint: -->
기본값, "Yes"와 "No" 라벨의 사용자 지정 문구, 안내용 힌트도 함께 지정할 수 있습니다.

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
필요한 경우 `required` 인수를 전달하여 사용자가 반드시 "Yes"를 선택하도록 요구할 수 있습니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수도 있습니다.

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
사용자가 미리 정의된 선택지 중 하나를 선택해야 한다면 `select` 함수를 사용할 수 있습니다.

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

<!-- You may also specify the default choice and an informational hint: -->
기본 선택지와 안내용 힌트도 지정할 수 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```
<!-- You may also pass an associative array to the `options` argument to have the selected key returned instead of its value: -->
`options` 인수에 연관 배열을 전달하여 선택된 값 대신 선택된 키가 반환되도록 할 수도 있습니다.

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

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument: -->
목록이 스크롤되기 전까지 최대 다섯 개의 옵션이 표시됩니다. `scroll` 인수를 전달하여 이 값을 사용자 지정할 수 있습니다.

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-info"></a>
<!-- #### Secondary Information -->
#### Secondary Information

<!-- The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`: -->
`info` 인수는 현재 강조 표시된 옵션에 대한 추가 정보를 표시하는 데 사용할 수 있습니다. 클로저를 제공하면 현재 강조 표시된 옵션의 값을 전달받으며, 문자열 또는 `null`을 반환해야 합니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    info: fn (string $value) => match ($value) {
        'member' => 'Can view and comment.',
        'contributor' => 'Can view, comment, and edit.',
        'owner' => 'Full access to all resources.',
        default => null,
    }
);
```

<!-- You may also pass a static string to the `info` argument if the information does not depend on the highlighted option: -->
정보가 강조 표시된 옵션에 따라 달라지지 않는다면 `info` 인수에 정적 문자열을 전달할 수도 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    info: 'The role may be changed at any time.'
);
```

<a name="select-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Unlike other prompt functions, the `select` function doesn't accept the `required` argument because it is not possible to select nothing. However, you may pass a closure to the `validate` argument if you need to present an option but prevent it from being selected: -->
다른 프롬프트 함수와 달리 `select` 함수는 `required` 인수를 받지 않습니다. 아무것도 선택하지 않는 것이 불가능하기 때문입니다. 하지만 옵션을 보여 주되 선택되지 못하게 해야 한다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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

<!-- If the `options` argument is an associative array, then the closure will receive the selected key, otherwise it will receive the selected value. The closure may return an error message, or `null` if the validation passes. -->
`options` 인수가 연관 배열이면 클로저는 선택된 키를 전달받고, 그렇지 않으면 선택된 값을 전달받습니다. 클로저는 오류 메시지를 반환하거나, 유효성 검증이 통과하면 `null`을 반환할 수 있습니다.

<a name="multiselect"></a>
<!-- ### Multi-select -->
### Multi-select

<!-- If you need the user to be able to select multiple options, you may use the `multiselect` function: -->
사용자가 여러 옵션을 선택할 수 있어야 한다면 `multiselect` 함수를 사용할 수 있습니다.

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

<!-- You may also specify default choices and an informational hint: -->
기본 선택값과 안내 힌트를 지정할 수도 있습니다.

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
`options` 인수에 연관 배열을 전달하여 선택된 옵션의 값 대신 키가 반환되도록 할 수도 있습니다.

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

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument: -->
목록이 스크롤되기 전까지 최대 다섯 개의 옵션이 표시됩니다. `scroll` 인수를 전달하여 이 값을 사용자 지정할 수 있습니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-info"></a>
<!-- #### Secondary Information -->
#### Secondary Information

<!-- The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`: -->
`info` 인수는 현재 강조 표시된 옵션에 대한 추가 정보를 표시하는 데 사용할 수 있습니다. 클로저를 제공하면 현재 강조 표시된 옵션의 값을 전달받으며, 문자열 또는 `null`을 반환해야 합니다.

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    info: fn (string $value) => match ($value) {
        'read' => 'View resources and their properties.',
        'create' => 'Create new resources.',
        'update' => 'Modify existing resources.',
        'delete' => 'Permanently remove resources.',
        default => null,
    }
);
```

<a name="multiselect-required"></a>
<!-- #### Requiring a Value -->
#### Requiring a Value

<!-- By default, the user may select zero or more options. You may pass the `required` argument to enforce one or more options instead: -->
기본적으로 사용자는 0개 이상의 옵션을 선택할 수 있습니다. 하나 이상의 옵션을 반드시 선택하도록 강제하려면 `required` 인수를 전달하면 됩니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

<!-- If you would like to customize the validation message, you may provide a string to the `required` argument: -->
유효성 검증 메시지를 사용자 지정하려면 `required` 인수에 문자열을 제공할 수 있습니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- You may pass a closure to the `validate` argument if you need to present an option but prevent it from being selected: -->
옵션을 보여 주되 선택되지 못하게 해야 한다면 `validate` 인수에 클로저를 전달할 수 있습니다.

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

<!-- If the `options` argument is an associative array then the closure will receive the selected keys, otherwise it will receive the selected values. The closure may return an error message, or `null` if the validation passes. -->
`options` 인수가 연관 배열이면 클로저는 선택된 키들을 전달받고, 그렇지 않으면 선택된 값들을 전달받습니다. 클로저는 오류 메시지를 반환하거나, 유효성 검증이 통과하면 `null`을 반환할 수 있습니다.

<a name="suggest"></a>
<!-- ### Suggest -->
### Suggest

<!-- The `suggest` function can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`suggest` 함수는 가능한 선택지에 대한 자동 완성을 제공하는 데 사용할 수 있습니다. 사용자는 자동 완성 힌트와 관계없이 어떤 답변이든 입력할 수 있습니다.

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `suggest` function. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far and return an array of options for auto-completion: -->
또는 `suggest` 함수의 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저는 사용자가 입력 문자를 입력할 때마다 호출됩니다. 클로저는 지금까지의 사용자 입력이 담긴 문자열 매개변수를 받아야 하며, 자동 완성 옵션 배열을 반환해야 합니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더 텍스트, 기본값, 안내 힌트를 함께 포함할 수도 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    placeholder: 'E.g. Taylor',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="suggest-info"></a>
<!-- #### Secondary Information -->
#### Secondary Information

<!-- The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`: -->
`info` 인수는 현재 강조 표시된 옵션에 대한 추가 정보를 표시하는 데 사용할 수 있습니다. 클로저를 제공하면 현재 강조 표시된 옵션의 값을 전달받으며, 문자열 또는 `null`을 반환해야 합니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    info: fn (string $value) => match ($value) {
        'Taylor' => 'Administrator',
        'Dayle' => 'Contributor',
        default => null,
    }
);
```

<a name="suggest-required"></a>
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
값을 반드시 입력받아야 한다면 `required` 인수를 전달할 수 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 사용자 지정하려면 문자열을 전달할 수도 있습니다.

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
마지막으로, 추가 유효성 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달할 수 있습니다.

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
클로저는 입력된 값을 전달받으며, 오류 메시지를 반환하거나 유효성 검증이 통과하면 `null`을 반환할 수 있습니다.

<!-- Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument: -->
또는 Laravel의 [validator](/docs/13.x/validation) 기능을 활용할 수도 있습니다. 이를 사용하려면 속성 이름과 원하는 유효성 검증 규칙을 담은 배열을 `validate` 인수에 제공하세요.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
<!-- ### Search -->
### Search

<!-- If you have a lot of options for the user to select from, the `search` function allows the user to type a search query to filter the results before using the arrow keys to select an option: -->
사용자가 선택해야 할 옵션이 많다면 `search` 함수를 사용하여 사용자가 검색어를 입력해 결과를 필터링한 뒤, 화살표 키로 옵션을 선택할 수 있게 할 수 있습니다.

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

<!-- The closure will receive the text that has been typed by the user so far and must return an array of options. If you return an associative array then the selected option's key will be returned, otherwise its value will be returned instead. -->
클로저는 사용자가 지금까지 입력한 텍스트를 전달받으며, 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 옵션의 키가 반환되고, 그렇지 않으면 값이 반환됩니다.

<!-- When filtering an array where you intend to return the value, you should use the `array_values` function or the `values` Collection method to ensure the array doesn't become associative: -->
값을 반환하려는 의도로 배열을 필터링할 때는 배열이 연관 배열이 되지 않도록 `array_values` 함수 또는 `values` Collection 메서드를 사용해야 합니다.

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

<!-- You may also include placeholder text and an informational hint: -->
플레이스홀더 텍스트와 안내 힌트를 함께 포함할 수도 있습니다.

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

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument: -->
목록이 스크롤되기 전까지 최대 다섯 개의 옵션이 표시됩니다. `scroll` 인수를 전달하여 이 값을 사용자 지정할 수 있습니다.

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-info"></a>
<!-- #### Secondary Information -->
#### Secondary Information

<!-- The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`: -->
`info` 인수는 현재 강조 표시된 옵션에 대한 추가 정보를 표시하는 데 사용할 수 있습니다. 클로저를 제공하면 현재 강조 표시된 옵션의 값을 전달받으며, 문자열 또는 `null`을 반환해야 합니다.

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    info: fn (int $userId) => User::find($userId)?->email
);
```

<a name="search-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- If you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
추가 유효성 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달할 수 있습니다.

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

<!-- If the `options` closure returns an associative array, then the closure will receive the selected key, otherwise, it will receive the selected value. The closure may return an error message, or `null` if the validation passes. -->
`options` 클로저가 연관 배열을 반환하면 클로저는 선택된 키를 전달받고, 그렇지 않으면 선택된 값을 전달받습니다. 클로저는 오류 메시지를 반환하거나, 유효성 검증이 통과하면 `null`을 반환할 수 있습니다.

<a name="multisearch"></a>
<!-- ### Multi-search -->
### Multi-search

<!-- If you have a lot of searchable options and need the user to be able to select multiple items, the `multisearch` function allows the user to type a search query to filter the results before using the arrow keys and space-bar to select options: -->
검색 가능한 옵션이 많고 사용자가 여러 항목을 선택할 수 있어야 한다면 `multisearch` 함수를 사용하여 사용자가 검색어를 입력해 결과를 필터링한 뒤, 화살표 키와 스페이스바로 옵션을 선택할 수 있게 할 수 있습니다.
```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

<!-- The closure will receive the text that has been typed by the user so far and must return an array of options. If you return an associative array then the selected options' keys will be returned; otherwise, their values will be returned instead. -->
클로저는 사용자가 지금까지 입력한 텍스트를 전달받으며, 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 옵션의 키가 반환됩니다. 그렇지 않으면 선택된 옵션의 값이 반환됩니다.

<!-- When filtering an array where you intend to return the value, you should use the `array_values` function or the `values` Collection method to ensure the array doesn't become associative: -->
값을 반환하려는 배열을 필터링할 때는 배열이 연관 배열로 바뀌지 않도록 `array_values` 함수나 `values` Collection 메서드를 사용해야 합니다.

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

<!-- You may also include placeholder text and an informational hint: -->
플레이스홀더 텍스트와 안내 힌트를 함께 포함할 수도 있습니다.

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

<!-- Up to five options will be displayed before the list begins to scroll. You may customize this by providing the `scroll` argument: -->
목록이 스크롤되기 전까지 최대 다섯 개의 옵션이 표시됩니다. `scroll` 인수를 제공하여 이 값을 사용자 정의할 수 있습니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-info"></a>
<!-- #### Secondary Information -->
#### Secondary Information

<!-- The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`: -->
`info` 인수는 현재 강조된 옵션에 대한 추가 정보를 표시하는 데 사용할 수 있습니다. 클로저를 제공하면 현재 강조된 옵션의 값을 전달받으며, 문자열 또는 `null`을 반환해야 합니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    info: fn (int $userId) => User::find($userId)?->email
);
```

<a name="multisearch-required"></a>
<!-- #### Requiring a Value -->
#### Requiring a Value

<!-- By default, the user may select zero or more options. You may pass the `required` argument to enforce one or more options instead: -->
기본적으로 사용자는 옵션을 하나도 선택하지 않거나 여러 개 선택할 수 있습니다. 하나 이상의 옵션을 반드시 선택하도록 하려면 `required` 인수를 전달하면 됩니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

<!-- If you would like to customize the validation message, you may also provide a string to the `required` argument: -->
유효성 검증 메시지를 사용자 정의하려면 `required` 인수에 문자열을 제공할 수도 있습니다.

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
<!-- #### Additional Validation -->
#### Additional Validation

<!-- If you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
추가 유효성 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달할 수 있습니다.

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

<!-- If the `options` closure returns an associative array, then the closure will receive the selected keys; otherwise, it will receive the selected values. The closure may return an error message, or `null` if the validation passes. -->
`options` 클로저가 연관 배열을 반환하면 이 클로저는 선택된 키를 전달받습니다. 그렇지 않으면 선택된 값을 전달받습니다. 클로저는 오류 메시지를 반환하거나, 유효성 검증을 통과한 경우 `null`을 반환할 수 있습니다.

<a name="pause"></a>
<!-- ### Pause -->
### Pause

<!-- The `pause` function may be used to display informational text to the user and wait for them to confirm their desire to proceed by pressing the Enter / Return key: -->
`pause` 함수는 사용자에게 안내 텍스트를 표시하고, 사용자가 Enter / Return 키를 눌러 계속 진행할 의사가 있음을 확인할 때까지 기다리는 데 사용할 수 있습니다.

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="autocomplete"></a>
<!-- ### Autocomplete -->
### Autocomplete

<!-- The `autocomplete` function can be used to provide inline auto-completion for possible choices. As the user types, suggestions that match their input will appear as ghost text that can be accepted by pressing `Tab` or the right arrow key: -->
`autocomplete` 함수는 가능한 선택지에 대해 인라인 자동 완성을 제공하는 데 사용할 수 있습니다. 사용자가 입력하면 입력값과 일치하는 제안이 고스트 텍스트로 표시되며, `Tab` 또는 오른쪽 화살표 키를 눌러 적용할 수 있습니다.

```php
use function Laravel\Prompts\autocomplete;

$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim']
);
```

<!-- You may also include placeholder text, a default value, and an informational hint: -->
플레이스홀더 텍스트, 기본값, 안내 힌트를 함께 포함할 수도 있습니다.

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    placeholder: 'E.g. Taylor',
    default: $user?->name,
    hint: 'Use tab to accept, up/down to cycle.'
);
```

<a name="autocomplete-closure"></a>
<!-- #### Dynamic Options -->
#### Dynamic Options

<!-- You may also pass a closure to dynamically generate options based on the user's input. The closure will be called each time the user types a character and should return an array of options for auto-completion: -->
사용자의 입력을 기반으로 옵션을 동적으로 생성하기 위해 클로저를 전달할 수도 있습니다. 이 클로저는 사용자가 문자를 입력할 때마다 호출되며, 자동 완성에 사용할 옵션 배열을 반환해야 합니다.

```php
$file = autocomplete(
    label: 'Which file?',
    options: fn (string $value) => collect($files)
        ->filter(fn ($file) => str_starts_with(strtolower($file), strtolower($value)))
        ->values()
        ->all(),
);
```

<a name="autocomplete-required"></a>
<!-- #### Required Values -->
#### Required Values

<!-- If you require a value to be entered, you may pass the `required` argument: -->
값을 반드시 입력해야 한다면 `required` 인수를 전달할 수 있습니다.

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    required: true
);
```

<!-- If you would like to customize the validation message, you may also pass a string: -->
유효성 검증 메시지를 사용자 정의하려면 문자열을 전달할 수도 있습니다.

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    required: 'Your name is required.'
);
```

<a name="autocomplete-validation"></a>
<!-- #### Additional Validation -->
#### Additional Validation

<!-- Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument: -->
마지막으로, 추가 유효성 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

<!-- The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes. -->
클로저는 입력된 값을 전달받으며, 오류 메시지를 반환하거나 유효성 검증을 통과한 경우 `null`을 반환할 수 있습니다.

<a name="transforming-input-before-validation"></a>
<!-- ## Transforming Input Before Validation -->
## Transforming Input Before Validation

<!-- Sometimes you may want to transform the prompt input before validation takes place. For example, you may wish to remove white space from any provided strings. To accomplish this, many of the prompt functions provide a `transform` argument, which accepts a closure: -->
때로는 유효성 검증이 수행되기 전에 프롬프트 입력값을 변환하고 싶을 수 있습니다. 예를 들어, 제공된 문자열에서 공백을 제거하고 싶을 수 있습니다. 이를 위해 여러 프롬프트 함수는 클로저를 받는 `transform` 인수를 제공합니다.

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
<!-- ## Forms -->
## Forms

<!-- Often, you will have multiple prompts that will be displayed in sequence to collect information before performing additional actions. You may use the `form` function to create a grouped set of prompts for the user to complete: -->
추가 작업을 수행하기 전에 정보를 수집하기 위해 여러 프롬프트를 순서대로 표시해야 하는 경우가 많습니다. `form` 함수를 사용하면 사용자가 완료할 프롬프트 묶음을 만들 수 있습니다.

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

<!-- The `submit` method will return a numerically indexed array containing all of the responses from the form's prompts. However, you may provide a name for each prompt via the `name` argument. When a name is provided, the named prompt's response may be accessed via that name: -->
`submit` 메서드는 폼의 프롬프트에서 받은 모든 응답을 숫자 인덱스 배열로 반환합니다. 하지만 `name` 인수를 통해 각 프롬프트에 이름을 지정할 수 있습니다. 이름이 제공되면 해당 이름으로 프롬프트의 응답에 접근할 수 있습니다.

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

<!-- The primary benefit of using the `form` function is the ability for the user to return to previous prompts in the form using `CTRL + U`. This allows the user to fix mistakes or alter selections without needing to cancel and restart the entire form. -->
`form` 함수를 사용할 때의 주요 장점은 사용자가 `CTRL + U`를 사용하여 폼의 이전 프롬프트로 돌아갈 수 있다는 점입니다. 이를 통해 사용자는 전체 폼을 취소하고 다시 시작할 필요 없이 실수를 수정하거나 선택을 변경할 수 있습니다.

<!-- If you need more granular control over a prompt in a form, you may invoke the `add` method instead of calling one of the prompt functions directly. The `add` method is passed all previous responses provided by the user: -->
폼 안의 프롬프트를 더 세밀하게 제어해야 한다면, 프롬프트 함수 중 하나를 직접 호출하는 대신 `add` 메서드를 호출할 수 있습니다. `add` 메서드에는 사용자가 이전에 제공한 모든 응답이 전달됩니다.

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
<!-- ## Informational Messages -->
## Informational Messages

<!-- The `note`, `info`, `warning`, `error`, and `alert` functions may be used to display informational messages: -->
`note`, `info`, `warning`, `error`, `alert` 함수는 안내 메시지를 표시하는 데 사용할 수 있습니다.

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<!-- The `table` function makes it easy to display multiple rows and columns of data. All you need to do is provide the column names and the data for the table: -->
`table` 함수를 사용하면 여러 행과 컬럼으로 이루어진 데이터를 쉽게 표시할 수 있습니다. 컬럼 이름과 테이블 데이터를 제공하기만 하면 됩니다.

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
<!-- ## Spin -->
## Spin

<!-- The `spin` function displays a spinner along with an optional message while executing a specified callback. It serves to indicate ongoing processes and returns the callback's results upon completion: -->
`spin` 함수는 지정된 콜백을 실행하는 동안 선택적 메시지와 함께 스피너를 표시합니다. 진행 중인 프로세스를 나타내는 역할을 하며, 완료되면 콜백의 결과를 반환합니다.

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> `spin` 함수는 스피너 애니메이션을 표시하기 위해 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 기능이 필요합니다. 이 확장 기능을 사용할 수 없는 경우에는 스피너의 정적 버전이 대신 표시됩니다.

<a name="progress"></a>
<!-- ## Progress Bars -->
## Progress Bars

<!-- For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `progress` function, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value: -->
오래 실행되는 작업에서는 작업이 얼마나 완료되었는지 사용자에게 알려주는 진행률 표시줄을 보여주는 것이 도움이 될 수 있습니다. `progress` 함수를 사용하면 Laravel은 진행률 표시줄을 표시하고, 주어진 iterable 값의 각 반복마다 진행률을 증가시킵니다.

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

<!-- The `progress` function acts like a map function and will return an array containing the return value of each iteration of your callback. -->
`progress` 함수는 map 함수처럼 동작하며, 콜백의 각 반복에서 반환된 값을 담은 배열을 반환합니다.

<!-- The callback may also accept the `Laravel\Prompts\Progress` instance, allowing you to modify the label and hint on each iteration: -->
콜백은 `Laravel\Prompts\Progress` 인스턴스를 함께 받을 수도 있습니다. 이를 통해 각 반복마다 라벨과 힌트를 수정할 수 있습니다.

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

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar via the `advance` method after processing each item: -->
때로는 진행률 표시줄을 어떻게 증가시킬지 더 수동으로 제어해야 할 수 있습니다. 먼저 프로세스가 반복할 총 단계 수를 정의합니다. 그런 다음 각 항목을 처리한 뒤 `advance` 메서드를 통해 진행률 표시줄을 증가시킵니다.

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

<a name="task"></a>
<!-- ## Task -->
## Task

<!-- The `task` function displays a labeled task with a spinner and a scrolling live output area while a given callback is executing. It is ideal for wrapping long-running processes such as dependency installation or deployment scripts, providing real-time visibility into what is happening: -->
`task` 함수는 주어진 콜백이 실행되는 동안 스피너와 스크롤되는 실시간 출력 영역을 포함한 라벨이 있는 작업을 표시합니다. 의존성 설치나 배포 스크립트처럼 오래 실행되는 프로세스를 감싸기에 적합하며, 현재 어떤 일이 일어나고 있는지 실시간으로 확인할 수 있게 해줍니다.

```php
use function Laravel\Prompts\task;

task(
    label: 'Installing dependencies',
    callback: function ($logger) {
        // Long-running process...
    }
);
```

<!-- The callback receives a `Logger` instance that you may use to display log lines, status messages, and streamed text in the task's output area. -->
콜백은 `Logger` 인스턴스를 전달받습니다. 이를 사용하여 작업의 출력 영역에 로그 라인, 상태 메시지, 스트리밍 텍스트를 표시할 수 있습니다.

> [!WARNING]
> `task` 함수는 스피너 애니메이션을 표시하기 위해 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 기능이 필요합니다. 이 확장 기능을 사용할 수 없는 경우에는 작업의 정적 버전이 대신 표시됩니다.

<a name="task-logging"></a>
<!-- #### Logging Lines -->
#### Logging Lines
<!-- The `line` method writes a single log line to the task's scrolling output area: -->
`line` 메서드는 작업의 스크롤되는 출력 영역에 로그 한 줄을 씁니다.

```php
task(
    label: 'Installing dependencies',
    callback: function ($logger) {
        $logger->line('Resolving packages...');
        // ...
        $logger->line('Downloading laravel/framework');
        // ...
    }
);
```

<a name="task-status-messages"></a>
<!-- #### Status Messages -->
#### Status Messages

<!-- You may use the `success`, `warning`, and `error` methods to display status messages. These appear as stable, highlighted messages above the scrolling log area: -->
`success`, `warning`, `error` 메서드를 사용하여 상태 메시지를 표시할 수 있습니다. 이 메시지는 스크롤되는 로그 영역 위에 고정된 강조 메시지로 나타납니다.

```php
task(
    label: 'Deploying application',
    callback: function ($logger) {
        $logger->line('Pulling latest changes...');
        // ...
        $logger->success('Changes pulled!');

        $logger->line('Running migrations...');
        // ...
        $logger->warning('No new migrations to run.');

        $logger->line('Clearing cache...');
        // ...
        $logger->success('Cache cleared!');
    }
);
```

<a name="task-label"></a>
<!-- #### Updating the Label -->
#### Updating the Label

<!-- The `label` method allows you to update the task's label while it is running: -->
`label` 메서드를 사용하면 작업이 실행되는 동안 작업의 레이블을 업데이트할 수 있습니다.

```php
task(
    label: 'Starting deployment...',
    callback: function ($logger) {
        $logger->label('Pulling latest changes...');
        // ...
        $logger->label('Running migrations...');
        // ...
        $logger->label('Clearing cache...');
        // ...
    }
);
```

<a name="task-sub-label"></a>
<!-- #### Displaying a Sub-Label -->
#### Displaying a Sub-Label

<!-- The `subLabel` method displays a dim line beneath the task's main label, which is useful for communicating ephemeral status such as the step currently in progress. Pass an empty string to clear the sub-label: -->
`subLabel` 메서드는 작업의 기본 레이블 아래에 흐리게 표시되는 줄을 보여줍니다. 현재 진행 중인 단계처럼 일시적인 상태를 전달할 때 유용합니다. 하위 레이블을 지우려면 빈 문자열을 전달합니다.

```php
task(
    label: 'Deploying',
    callback: function ($logger) {
        $logger->subLabel('Building assets...');
        // ...
        $logger->subLabel('Running migrations...');
        // ...
        $logger->subLabel('');
    }
);
```

<!-- You may also provide an initial sub-label via the `subLabel` argument: -->
`subLabel` 인수를 통해 초기 하위 레이블을 제공할 수도 있습니다.

```php
task(
    label: 'Deploying',
    callback: function ($logger) {
        // ...
    },
    subLabel: 'Preparing...'
);
```

<a name="task-streaming"></a>
<!-- #### Streaming Text -->
#### Streaming Text

<!-- For processes that produce output incrementally, such as AI-generated responses, the `partial` method allows you to stream text word-by-word or chunk-by-chunk. Once the stream is complete, call `commitPartial` to finalize the output: -->
AI 생성 응답처럼 출력이 점진적으로 생성되는 프로세스에서는 `partial` 메서드를 사용해 텍스트를 단어 단위 또는 청크 단위로 스트리밍할 수 있습니다. 스트림이 완료되면 `commitPartial`을 호출하여 출력을 확정합니다.

```php
task(
    label: 'Generating response...',
    callback: function ($logger) {
        foreach ($words as $word) {
            $logger->partial($word . ' ');
        }

        $logger->commitPartial();
    }
);
```

<a name="task-limit"></a>
<!-- #### Customizing the Output Limit -->
#### Customizing the Output Limit

<!-- By default, the task displays up to 10 lines of scrolling output. You may customize this via the `limit` argument: -->
기본적으로 작업은 스크롤되는 출력을 최대 10줄까지 표시합니다. `limit` 인수를 통해 이를 사용자 정의할 수 있습니다.

```php
task(
    label: 'Installing dependencies',
    callback: function ($logger) {
        // ...
    },
    limit: 20
);
```

<a name="task-keep-summary"></a>
<!-- #### Keeping the Summary -->
#### Keeping the Summary

<!-- By default, the task's output is erased once the callback finishes. If you would like to keep the status messages on screen after the task has completed, you may pass the `keepSummary` argument: -->
기본적으로 작업의 출력은 콜백이 완료되면 지워집니다. 작업이 완료된 후에도 상태 메시지를 화면에 유지하려면 `keepSummary` 인수를 전달할 수 있습니다.

```php
task(
    label: 'Deploying',
    callback: function ($logger) {
        $logger->success('Assets built');
        // ...
        $logger->success('Migrations complete');
    },
    keepSummary: true,
);
```

<a name="stream"></a>
<!-- ## Stream -->
## Stream

<!-- The `stream` function displays text that streams into the terminal, ideal for displaying AI-generated content or any text that arrives incrementally: -->
`stream` 함수는 터미널로 스트리밍되는 텍스트를 표시합니다. AI 생성 콘텐츠나 점진적으로 도착하는 텍스트를 표시하는 데 적합합니다.

```php
use function Laravel\Prompts\stream;

$stream = stream();

foreach ($words as $word) {
    $stream->append($word . ' ');
    usleep(25_000); // Simulate delay between chunks...
}

$stream->close();
```

<!-- The `append` method adds text to the stream, rendering it with a gradual fade-in effect. When all content has been streamed, call the `close` method to finalize the output and restore the cursor. -->
`append` 메서드는 스트림에 텍스트를 추가하고, 점진적인 페이드인 효과와 함께 렌더링합니다. 모든 콘텐츠가 스트리밍되면 `close` 메서드를 호출하여 출력을 확정하고 커서를 복원합니다.

<a name="terminal-title"></a>
<!-- ## Terminal Title -->
## Terminal Title

<!-- The `title` function updates the title of the user's terminal window or tab: -->
`title` 함수는 사용자의 터미널 창 또는 탭 제목을 업데이트합니다.

```php
use function Laravel\Prompts\title;

title('Installing Dependencies');
```

<!-- To reset the terminal title back to its default, pass an empty string: -->
터미널 제목을 기본값으로 되돌리려면 빈 문자열을 전달합니다.

```php
title('');
```

<a name="clear"></a>
<!-- ## Clearing the Terminal -->
## Clearing the Terminal

<!-- The `clear` function may be used to clear the user's terminal: -->
`clear` 함수는 사용자의 터미널을 지우는 데 사용할 수 있습니다.

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
<!-- ## Terminal Considerations -->
## Terminal Considerations

<a name="terminal-width"></a>
<!-- #### Terminal Width -->
#### Terminal Width

<!-- If the length of any label, option, or validation message exceeds the number of "columns" in the user's terminal, it will be automatically truncated to fit. Consider minimizing the length of these strings if your users may be using narrower terminals. A typically safe maximum length is 74 characters to support an 80-character terminal. -->
레이블, 옵션, 유효성 검증 메시지의 길이가 사용자의 터미널 "컬럼" 수를 초과하면, 맞게 표시되도록 자동으로 잘립니다. 사용자가 더 좁은 터미널을 사용할 수 있다면 이러한 문자열의 길이를 줄이는 것을 고려하세요. 일반적으로 80자 터미널을 지원하기 위한 안전한 최대 길이는 74자입니다.

<a name="terminal-height"></a>
<!-- #### Terminal Height -->
#### Terminal Height

<!-- For any prompts that accept the `scroll` argument, the configured value will automatically be reduced to fit the height of the user's terminal, including space for a validation message. -->
`scroll` 인수를 받는 모든 프롬프트에서는 설정된 값이 사용자의 터미널 높이에 맞게 자동으로 줄어듭니다. 이때 유효성 검증 메시지를 위한 공간도 포함됩니다.

<a name="fallbacks"></a>
<!-- ## Unsupported Environments and Fallbacks -->
## Unsupported Environments and Fallbacks

<!-- Laravel Prompts supports macOS, Linux, and Windows with WSL. Due to limitations in the Windows version of PHP, it is not currently possible to use Laravel Prompts on Windows outside of WSL. -->
Laravel Prompts는 macOS, Linux, 그리고 WSL이 있는 Windows를 지원합니다. Windows 버전 PHP의 제한 사항 때문에, 현재 WSL 밖의 Windows에서는 Laravel Prompts를 사용할 수 없습니다.

<!-- For this reason, Laravel Prompts supports falling back to an alternative implementation such as the [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html). -->
이러한 이유로 Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)와 같은 대체 구현으로 폴백하는 기능을 지원합니다.

> [!NOTE]
> Laravel 프레임워크와 함께 Laravel Prompts를 사용할 때는 각 프롬프트의 폴백이 이미 구성되어 있으며, 지원되지 않는 환경에서 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
<!-- #### Fallback Conditions -->
#### Fallback Conditions

<!-- If you are not using Laravel or need to customize when the fallback behavior is used, you may pass a boolean to the `fallbackWhen` static method on the `Prompt` class: -->
Laravel을 사용하지 않거나 폴백 동작이 사용되는 시점을 사용자 정의해야 한다면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 boolean 값을 전달할 수 있습니다.

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
Laravel을 사용하지 않거나 폴백 동작을 사용자 정의해야 한다면, 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달할 수 있습니다.

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

<!-- Fallbacks must be configured individually for each prompt class. The closure will receive an instance of the prompt class and must return an appropriate type for the prompt. -->
폴백은 각 프롬프트 클래스마다 개별적으로 구성해야 합니다. 클로저는 프롬프트 클래스의 인스턴스를 받고, 해당 프롬프트에 적절한 타입을 반환해야 합니다.

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Laravel provides a variety of methods for testing that your command displays the expected Prompt messages: -->
Laravel은 명령어가 예상한 Prompt 메시지를 표시하는지 테스트할 수 있는 다양한 메서드를 제공합니다.

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
