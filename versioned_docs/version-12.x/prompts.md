# 프롬프트 (Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트 영역](#textarea)
    - [숫자](#number)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [추천](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시정지](#pause)
- [유효성 검증 전 입력값 변환](#transforming-input-before-validation)
- [폼](#forms)
- [정보 메시지](#informational-messages)
- [테이블](#tables)
- [스핀](#spin)
- [진행률 바](#progress)
- [터미널 초기화](#clear)
- [터미널 관련 고려 사항](#terminal-considerations)
- [지원되지 않는 환경 및 대체 동작](#fallbacks)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 브라우저와 유사한 플레이스홀더 텍스트 및 유효성 검증 등 아름답고 사용자 친화적인 폼을 쉽게 추가할 수 있도록 해주는 PHP 패키지입니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/12.x/artisan#writing-commands)에서 사용자 입력을 받을 때 특히 유용하지만, 모든 명령줄 기반 PHP 프로젝트에서 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, Windows(WSL 환경)를 지원합니다. 더 자세한 내용은 [지원되지 않는 환경 및 대체 동작](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

Laravel Prompts는 최신 Laravel 릴리스에 기본 포함되어 있습니다.

다른 PHP 프로젝트에도 Composer 패키지 관리자를 이용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트 (Available Prompts)

<a name="text"></a>
### 텍스트 (Text)

`text` 함수는 지정한 질문을 사용자에게 표시하고, 입력값을 받아 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더 텍스트, 기본값, 추가 안내 문구도 설정할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수 입력값 지정

입력이 반드시 필요하다면, `required` 인수를 전달하세요:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 검증 메시지를 사용자 지정하려면 문자열을 전달할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증이 필요하다면, `validate` 인수에 클로저(익명 함수)를 전달할 수 있습니다:

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

이 클로저는 사용자가 입력한 값을 전달받아, 에러 메시지를 반환하거나 유효하다면 `null`을 반환합니다.

또는, Laravel의 [유효성 검증기](/docs/12.x/validation) 기능을 사용할 수도 있습니다. 이 경우 검증할 속성명과 검증 규칙이 포함된 배열을 `validate` 인수로 전달하면 됩니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트 영역 (Textarea)

`textarea` 함수는 사용자가 여러 줄로 입력할 수 있는 textarea로 질문을 던지고, 입력값을 받아 반환합니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 추가 안내 문구도 설정 가능합니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 입력값 지정

입력이 필수인 경우, `required` 인수를 사용합니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

유효성 메시지를 직접 지정하려면 문자열을 입력하세요:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증이 필요하다면, `validate` 인수에 클로저를 전달할 수 있습니다:

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

이 클로저는 입력값을 받아 에러 메시지 또는 `null`을 반환합니다.

또는 Laravel [유효성 검증기](/docs/12.x/validation)를 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="number"></a>
### 숫자 (Number)

`number` 함수는 질문을 표시하고, 숫자 입력을 받아 반환합니다. 사용자는 위/아래 방향키로 숫자를 조정할 수 있습니다:

```php
use function Laravel\Prompts\number;

$number = number('How many copies would you like?');
```

플레이스홀더, 기본값, 안내 문구도 사용할 수 있습니다:

```php
$name = number(
    label: 'How many copies would you like?',
    placeholder: '5',
    default: 1,
    hint: 'This will be determine how many copies to create.'
);
```

<a name="number-required"></a>
#### 필수 입력값 지정

입력이 필수인 경우, `required` 인수를 사용합니다:

```php
$copies = number(
    label: 'How many copies would you like?',
    required: true
);
```

유효성 메시지를 직접 지정하려면 문자열을 입력하세요:

```php
$copies = number(
    label: 'How many copies would you like?',
    required: 'A number of copies is required.'
);
```

<a name="number-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증이 필요하면, `validate` 인수에 클로저를 전달할 수 있습니다:

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

클로저는 입력값을 받아서 에러 메시지나 `null`을 반환합니다.

또는 Laravel [유효성 검증기](/docs/12.x/validation)를 활용할 수 있습니다:

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: ['copies' => 'required|integer|min:1|max:100']
);
```

<a name="password"></a>
### 비밀번호 (Password)

`password` 함수는 `text` 함수와 비슷하지만, 사용자가 입력하는 값이 콘솔에서 마스킹(숨김) 처리됩니다. 비밀번호 등 민감한 정보를 입력받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 안내 문구도 추가할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 입력값 지정

입력이 필수라면 `required` 인수를 사용하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

메시지를 직접 지정하려면 문자열을 입력합니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검증

추가 검증이 필요하다면, `validate` 인수에 클로저를 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

클로저는 입력값을 받아 에러 메시지 또는 `null`을 반환합니다.

또는 Laravel [유효성 검증기](/docs/12.x/validation)를 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인 (Confirm)

사용자에게 "예/아니오" 형태의 확인을 요청하고 싶을 때 `confirm` 함수를 사용할 수 있습니다. 사용자는 방향키나 `y`, `n` 키로 선택합니다. 결과는 `true` 또는 `false`로 반환됩니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "Yes"/"No" 버튼의 텍스트, 안내문도 지정할 수 있습니다:

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
#### "예" 필수 선택

필요하다면 사용자가 반드시 "예"를 선택하도록 요구할 수 있습니다. 이때 `required` 인수를 전달하세요:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

메시지를 사용자 정의하려면 문자열로 지정할 수도 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택 (Select)

사용자가 미리 정해진 항목 중에서 하나를 선택하도록 하려면 `select` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값과 안내 문구도 지정할 수 있습니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

연관 배열을 `options` 인수에 전달하면, 선택된 key가 반환됩니다:

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

최대 5개의 옵션이 리스트에 표시되며, 스크롤이 필요한 경우 `scroll` 인수로 제한을 변경할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검증

`select` 함수는 기본적으로 `required` 인수를 지원하지 않습니다(아무 것도 선택하지 않을 수 없기 때문). 하지만 특정 항목을 보이지만 선택을 막고 싶다면, `validate` 인수에 클로저를 전달할 수 있습니다:

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

`options` 인수가 연관 배열이면 선택된 키를, 배열이면 값을 반환합니다. 클로저는 에러 메시지나 `null`을 반환할 수 있습니다.

<a name="multiselect"></a>
### 다중 선택 (Multi-select)

여러 옵션 중 복수 개를 선택하게 하려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 안내 문구도 지정할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

연관 배열을 `options`로 전달하면 선택된 옵션의 키가 반환됩니다:

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

5개까지 옵션이 표시되고, 스크롤 수를 `scroll` 인수로 변경할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 값 선택 필수화

기본적으로 0개 이상의 항목을 선택할 수 있습니다. 최소 1개 이상을 필수로 선택하도록 하려면 `required` 인수를 사용하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

검증 메시지를 직접 넣으려면, 문자열로 `required`를 전달할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검증

특정 옵션을 선택하지 못하게 하려면 `validate` 인수에 클로저를 전달하세요:

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

연관 배열을 사용한다면 선택된 키들이, 단순 배열이면 값들이 전달됩니다. 반환값은 에러 메시지 또는 `null`입니다.

<a name="suggest"></a>
### 추천 (Suggest)

`suggest` 함수는 자동완성 후보를 제공할 수 있습니다. 자동완성 후보와 상관없이 사용자는 임의의 답변도 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는, 두 번째 인수로 클로저를 전달해 사용자가 입력할 때마다 자동완성 후보를 동적으로 제시할 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 문구도 지정할 수 있습니다:

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
#### 필수 입력값 지정

값 입력이 필수라면 `required`를 사용합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

메시지 지정도 가능합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검증

추가 검증이 필요하다면 클로저를 활용하세요:

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

또는 [유효성 검증기](/docs/12.x/validation)를 사용할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색 (Search)

옵션이 많을 때, `search` 함수는 사용자가 검색어를 입력해 목록을 필터링한 후, 원하는 항목을 선택할 수 있게 해줍니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 입력된 검색어를 받아 옵션 배열을 반환해야 합니다. 연관 배열 반환 시 선택된 키, 단순 배열이면 값을 반환합니다.

값을 반환하는 배열을 필터링할 때는 배열이 연관 배열로 변경되지 않도록 `array_values` 함수나 컬렉션의 `values` 메서드를 같이 사용하세요:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: 'Search for the user that should receive the mail',
    options: fn ($value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더, 안내 문구도 추가할 수 있습니다:

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

최대 5개 항목이 표시되며, `scroll` 인수로 조정할 수 있습니다:

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
#### 추가 유효성 검증

추가 검증이 필요하다면 `validate` 인수에 클로저를 사용할 수 있습니다:

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

연관 배열 반환인 경우 선택된 키, 값 배열이면 선택된 값을 전달받습니다.

<a name="multisearch"></a>
### 다중 검색 (Multi-search)

검색 가능한 여러 옵션 중 복수 항목을 선택해야 한다면 `multisearch` 함수를 사용하세요. 사용자는 검색어로 목록을 필터링하고, 방향키와 스페이스바로 원하는 항목을 선택할 수 있습니다.

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 입력된 검색어를 받아 배열을 반환해야 하며, 연관 배열이면 선택된 키 배열, 값 배열이면 선택된 값 배열을 반환합니다.

배열이 연관 배열이 되지 않도록, 값 배열 필터 시 `array_values` 또는 컬렉션의 `values` 메서드를 사용하세요:

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

플레이스홀더와 안내 문구도 추가할 수 있습니다:

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

5개까지 표시되고, `scroll` 인수로 조정할 수 있습니다:

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
#### 값 선택 필수화

기본적으로 0개 이상의 항목을 선택할 수 있습니다. 하나 이상을 필수로 요구하려면 `required` 인수를 사용하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

문자열로 메시지를 지정할 수도 있습니다:

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
#### 추가 유효성 검증

검증이 필요하면 클로저를 `validate` 인수에 전달하세요:

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

연관 배열이면 선택된 키 배열, 값 배열이면 선택된 값 배열을 전달받습니다. 반환값은 에러 메시지 또는 `null`입니다.

<a name="pause"></a>
### 일시정지 (Pause)

`pause` 함수는 중간 안내 메시지를 표시하고, 사용자가 Enter/Return을 눌러 진행하도록 합니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검증 전 입력값 변환 (Transforming Input Before Validation)

입력값에서 앞뒤 공백을 제거하는 등, 유효성 검증 전에 입력값을 가공(변환)하고 싶을 때가 있습니다. 이를 위해 많은 프롬프트 함수들은 `transform` 인수를 지원합니다. 이 인수는 클로저를 받아 입력값을 조작하게 할 수 있습니다:

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
## 폼 (Forms)

여러 개의 프롬프트를 순차적으로 보여주며 정보를 받은 후, 이후에 추가 동작을 수행하고 싶을 때가 많습니다. `form` 함수를 사용하면 여러 프롬프트를 그룹화하여 한 번에 사용자로부터 입력을 받을 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼의 응답값들을 숫자 인덱스 배열로 반환합니다. 하지만, 각 프롬프트에 `name` 인수를 부여하여 해당 이름의 키로 결과를 가져올 수도 있습니다:

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

`form` 함수의 가장 큰 장점은 사용자가 `CTRL + U` 단축키로 이전 프롬프트 단계로 돌아가 잘못된 입력을 수정하거나 선택을 변경할 수 있다는 점입니다. 사용자는 입력을 취소하지 않고도 전체 폼을 다시 시작할 필요 없이 개별 항목을 바로 수정할 수 있습니다.

폼 내부 프롬프트를 더 세밀하게 제어하고 싶을 때는, 각 프롬프트 함수 대신 `add` 메서드를 사용할 수 있습니다. 이때 기존 응답값들이 인수로 전달됩니다:

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
## 정보 메시지 (Informational Messages)

`note`, `info`, `warning`, `error`, `alert` 함수들은 다양한 정보성 메시지를 보여주기 위해 사용할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 (Tables)

`table` 함수는 여러 행과 열로 구성된 데이터를 쉽게 표시할 수 있게 해줍니다. 컬럼(header) 이름 배열과 데이터 배열만 넘기면 됩니다:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀 (Spin)

`spin` 함수는 작업이 진행 중일 때 스피너와 함께 선택적 메시지를 표시하며, 지정한 콜백이 끝나면 결과값을 반환합니다. 주로 시간이 소요되는 작업을 진행중임을 표시할 때 사용합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> 스피너 애니메이션을 표시하려면 PHP의 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장 모듈이 설치되어 있어야 합니다. 해당 확장이 없으면 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행률 바 (Progress Bars)

시간이 오래 걸리는 작업을 진행할 때, 사용자가 작업 완료 상태를 알 수 있도록 `progress` 함수를 활용할 수 있습니다. 이 함수는 주어진 반복가능(Iterable) 객체를 순회하면서 자동으로 진행률 바를 그려줍니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 map 함수처럼 동작하며, 콜백 반환값으로 이루어진 배열을 반환합니다.

콜백 함수에서 `Laravel\Prompts\Progress` 인스턴스를 받아, 각 반복마다 라벨과 안내 문구를 동적으로 수정할 수도 있습니다:

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

진행률 막대를 수동으로 제어하고 싶을 때에는, 먼저 처리해야 할 총 반복 횟수(steps)를 지정하고, 각 항목 처리 후 `advance` 메서드로 직접 진행률을 증가시킬 수 있습니다:

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
## 터미널 초기화 (Clearing the Terminal)

`clear` 함수는 사용자의 터미널 화면을 초기화할 수 있습니다:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 관련 고려 사항 (Terminal Considerations)

<a name="terminal-width"></a>
#### 터미널 너비

라벨, 옵션, 검증 메시지 등의 길이가 사용자의 터미널 열(Columns) 수를 초과할 경우, 해당 텍스트는 화면에 맞게 자동으로 잘립니다. 사용자가 좁은 터미널에서 사용할 수 있음을 고려해 이 텍스트의 길이를 너무 길게 만들지 않는 것이 좋습니다. 일반적으로 80자 터미널을 지원하기 위해 74자 이내가 안전합니다.

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인수를 지원하는 프롬프트에서, 설정한 표시 라인 개수는 터미널 높이에 맞게 자동으로 조정됩니다. 유효성 메시지 표시 공간 또한 고려됩니다.

<a name="fallbacks"></a>
## 지원되지 않는 환경 및 대체 동작 (Unsupported Environments and Fallbacks)

Laravel Prompts는 macOS, Linux, Windows(WSL 환경)를 지원합니다. Windows의 PHP 환경 제약으로 인해, 현재 WSL 이외의 Windows 환경에서는 Laravel Prompts를 사용할 수 없습니다.

이러한 이유로, Laravel Prompts는 대체 구현체(예: [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html))로 대체 동작이 가능하도록 설계되어 있습니다.

> [!NOTE]
> Laravel 프레임워크에서 Prompts를 사용할 경우, 각 프롬프트별 대체 구현이 미리 설정되어 있어 지원되지 않는 환경에서 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 동작 활성화 조건

Laravel이 아닌 환경에서 실행하거나, 대체 동작 시점을 커스텀으로 제어하려면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언 값을 전달하세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작 방식 커스텀

Laravel 환경이 아니거나, 대체 동작 자체를 커스텀 하고 싶다면 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달할 수 있습니다:

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

이 대체 동작은 각 프롬프트 클래스별로 따로 설정해야 합니다. 해당 클로저는 프롬프트 클래스 인스턴스를 인수로 받아 적절한 반환값을 돌려야 합니다.

<a name="testing"></a>
## 테스트 (Testing)

Laravel은 명령어에서 기대하는 프롬프트 메시지가 제대로 출력되는지 확인할 수 있도록 다양한 테스트 메서드를 제공합니다:

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
