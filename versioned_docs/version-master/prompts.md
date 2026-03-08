# 프롬프트 (Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트영역](#textarea)
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
- [안내 메시지](#informational-messages)
- [테이블](#tables)
- [스핀](#spin)
- [진행률 바](#progress)
- [터미널 화면 지우기](#clear)
- [터미널 관련 참고사항](#terminal-considerations)
- [지원되지 않는 환경 및 대체 동작](#fallbacks)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 아름답고 사용하기 쉬운 폼을 추가할 수 있는 PHP 패키지입니다. 브라우저와 유사한 플레이스홀더 텍스트와 유효성 검증 등의 기능을 제공합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/master/artisan#writing-commands)에서 사용자 입력을 받을 때 매우 적합하며, 모든 명령줄 기반 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, WSL(Windows Subsystem for Linux)이 설치된 Windows를 지원합니다. 자세한 내용은 [지원되지 않는 환경 및 대체 동작](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

Laravel Prompts는 최신 Laravel 버전에는 이미 포함되어 있습니다.

Laravel 이외의 PHP 프로젝트에서도 Composer 패키지 매니저를 사용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트 (Available Prompts)

<a name="text"></a>
### 텍스트

`text` 함수는 사용자에게 지정된 질문을 표시하고, 입력을 받아 반환합니다.

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더 텍스트, 기본값, 안내 힌트도 추가할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수 값 입력

값 입력을 필수로 지정하려면 `required` 인수를 전달하세요.

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 검증 메시지를 직접 지정하려면 문자열로 전달할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검증

추가적으로 유효성 검증 로직이 필요하다면, `validate` 인수에 클로저를 전달할 수 있습니다:

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

클로저는 사용자가 입력한 값을 받아 유효하지 않은 경우 에러 메시지를 반환하고, 통과하면 `null`을 반환합니다.

또한, Laravel의 [validator](/docs/master/validation) 기능을 활용할 수도 있습니다. 이를 위해 `validate` 인수에 속성명과 유효성 규칙을 배열로 전달합니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트영역

`textarea` 함수는 사용자에게 질문을 보여주고, 여러 줄 입력을 받아 반환합니다.

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 안내 힌트도 제공할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 값 입력

입력값을 필수로 지정하고 싶다면 `required` 인수를 사용하세요:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

유효성 검증 메시지를 직접 입력하려면 문자열로 지정합니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검증

클로저를 사용해 추가 유효성 검증을 할 수 있습니다:

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

클로저는 입력값을 받아 에러 메시지나 `null`을 반환합니다.

또한, Laravel의 [validator](/docs/master/validation) 기능도 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="number"></a>
### 숫자

`number` 함수는 사용자가 숫자를 입력하도록 유도하며, 입력값을 반환합니다. 사용자는 숫자 입력 칸에서 방향키(↑/↓)로 값을 조정할 수도 있습니다:

```php
use function Laravel\Prompts\number;

$number = number('How many copies would you like?');
```

플레이스홀더, 기본값, 안내 힌트도 사용할 수 있습니다:

```php
$name = number(
    label: 'How many copies would you like?',
    placeholder: '5',
    default: 1,
    hint: 'This will be determine how many copies to create.'
);
```

<a name="number-required"></a>
#### 필수 값 입력

입력을 필수로 지정하려면 `required` 인수를 사용하세요:

```php
$copies = number(
    label: 'How many copies would you like?',
    required: true
);
```

유효성 메시지를 직접 지정하려면 문자열을 사용하세요:

```php
$copies = number(
    label: 'How many copies would you like?',
    required: 'A number of copies is required.'
);
```

<a name="number-validation"></a>
#### 추가 유효성 검증

클로저를 이용해 추가 검증 로직을 정의할 수 있습니다:

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

또한 Laravel의 [validator](/docs/master/validation) 기능을 사용할 수 있습니다:

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: ['copies' => 'required|integer|min:1|max:100']
);
```

<a name="password"></a>
### 비밀번호

`password` 함수는 `text` 함수와 유사하지만, 입력값이 콘솔에서 마스킹(가려짐) 처리됩니다. 민감 정보, 예를 들어 비밀번호를 입력받을 때 적합합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더, 안내 힌트를 추가할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값 입력

입력이 필수라면 `required` 인수를 사용하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

직접 메시지를 지정할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검증

클로저를 이용해 유효성 검증을 추가할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

Laravel의 [validator](/docs/master/validation)도 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인

사용자에게 "예/아니요"와 같은 확인을 요청하려면 `confirm` 함수를 사용하세요. 사용자는 방향키로 선택하거나 `y` 또는 `n`을 눌러 응답할 수 있습니다. 반환값은 `true` 또는 `false`입니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예/아니요" 레이블의 커스터마이즈, 안내 힌트도 지정할 수 있습니다:

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
#### "예" 선택 강제

필요하다면, 사용자가 "예"를 반드시 선택하도록 `required` 인수를 사용할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

검증 메시지를 직접 지정할 수도 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택

미리 정의된 선택지 목록에서 하나를 선택하도록 하려면 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본값, 안내 힌트도 지정 가능합니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

선택 항목의 키(key)를 반환받으려면 연관 배열을 사용할 수 있습니다:

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

최대 다섯 개 옵션까지 한 번에 표시되며, `scroll` 인수를 사용해 표시 개수를 늘릴 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검증

다른 프롬프트 함수들과 달리, `select` 함수는 `required` 인수를 받지 않습니다. 무조건 하나는 선택해야 하기 때문입니다. 하지만 특정 선택을 제약하고 싶다면 `validate` 클로저를 사용할 수 있습니다:

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

`options`가 연관 배열이면 선택한 키가, 아니면 선택한 값이 클로저로 전달됩니다. 클로저는 에러 메시지나 `null`을 반환합니다.

<a name="multiselect"></a>
### 다중 선택

여러 옵션을 선택받으려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 안내 힌트도 사용할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

선택한 값 대신 키(Array key)를 반환하도록 연관 배열을 사용할 수도 있습니다:

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

최대 다섯 개 옵션까지 한 번에 표시되며, `scroll` 인수로 개수 지정 가능합니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 필수값 지정

기본적으로 사용자는 아무거나, 혹은 아무것도 선택하지 않을 수 있습니다. 꼭 하나 이상을 선택받으려면 `required` 인수를 사용하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

검증 메시지를 커스터마이징하려면 문자열로 전달할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검증

선택할 수 없는 옵션을 지정하고 싶다면, `validate` 클로저를 전달합니다:

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

`options`가 연관 배열이면 선택된 키 배열이, 아니면 값 배열이 전달됩니다.

<a name="suggest"></a>
### 추천

`suggest` 함수는 자동 완성(추천) 기능을 제공합니다. 사용자는 추천 목록과 상관없이 어떤 답변이든 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

혹은 두 번째 인수로 클로저를 전달하면, 사용자가 입력할 때마다 클로저가 호출되고, 입력값에 따라 추천 항목을 동적으로 구성할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 힌트도 사용할 수 있습니다:

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
#### 필수 값 입력

입력을 필수로 지정하려면 `required` 인수를 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

검증 메시지를 직접 지정할 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검증

클로저를 사용하여 추가 검증 로직을 정의할 수 있습니다:

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

또는 Laravel의 [validator](/docs/master/validation)를 활용할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색

선택 항목이 많은 경우, `search` 함수로 사용자가 검색어를 입력해 결과를 필터링한 후 선택할 수 있습니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자의 입력값을 받아, 선택 목록(배열)을 반환해야 합니다. 연관 배열을 반환하면 선택된 항목의 키, 일반 배열이면 값이 반환됩니다.

값의 배열에서 값을 반환할 때에는 `array_values` 또는 컬렉션의 `values` 메서드를 사용해 배열이 연관 배열이 되지 않도록 해야 합니다:

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

플레이스홀더, 안내 힌트도 사용할 수 있습니다:

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

최대 다섯 개 항목까지 한 번에 표시되며, `scroll` 인수로 표시 개수를 늘릴 수 있습니다:

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

추가 검증이 필요하다면 `validate`에 클로저를 전달하세요:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function ($value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return 'This user has opted-out of receiving mail.';
        }
    }
);
```

클로저는 선택된 키나 값(연관 배열 여부에 따라)을 인수로 받아, 에러 메시지나 `null`을 반환합니다.

<a name="multisearch"></a>
### 다중 검색

선택 항목이 많으면서, 여러 개를 검색·선택해야 할 경우 `multisearch` 함수로 사용자가 검색어를 입력·필터링 후 여러 항목을 화살표 및 스페이스바로 선택하게 할 수 있습니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

반환값은 선택된 키 배열(연관 배열일 경우) 또는 값 배열입니다.

값 배열을 필터링할 때는 순차 배열로 강제해야 합니다:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더, 안내 힌트도 사용할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

최대 다섯 개 항목까지 한 번에 표시되며, `scroll` 인수로 표시 개수를 늘릴 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-required"></a>
#### 필수 값 지정

아무 항목도 선택하지 않아도 되지만, 하나 이상 필수로 선택받으려면 `required` 인수를 사용하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

커스텀 검증 메시지 지정도 가능합니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>
#### 추가 유효성 검증

필요하다면 추가 검증 로직을 클로저로 작성할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
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

<a name="pause"></a>
### 일시정지

`pause` 함수는 사용자에게 안내 문구를 제공하고, 사용자가 엔터(Enter) 키를 눌러 계속 진행하기를 기다립니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검증 전 입력값 변환 (Transforming Input Before Validation)

프롬프트에서 받은 입력값을 유효성 검증 전에 변환하고 싶을 때가 있습니다. 예를 들어, 문자열 앞뒤의 공백을 제거하려 할 수 있습니다. 이를 위해 여러 프롬프트 함수들은 `transform` 인수를 제공합니다:

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

여러 프롬프트를 연속적으로 보여주고, 필요한 정보를 모두 수집한 뒤 추가 작업을 하고 싶을 때가 많습니다. 이럴 경우 `form` 함수를 이용해 프롬프트 그룹을 만들 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼의 각 프롬프트에 대한 응답을 숫자 인덱스 배열로 반환합니다. 각 프롬프트에 `name` 인수를 지정하면, 해당 이름으로 응답을 참조할 수 있습니다:

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

`form` 함수의 주요 장점은 사용자가 `CTRL + U`(Ctrl+U)를 이용해 이전 프롬프트로 돌아가서, 실수나 선택을 다시 수정할 수 있다는 점입니다. 폼 전체를 취소하고 다시 시작할 필요 없이 쉽게 수정 가능합니다.

폼 내에서 더 세밀하게 프롬프트를 제어하고 싶다면, 프롬프트 함수를 직접 호출하는 대신 `add` 메서드를 사용할 수도 있습니다. `add`의 클로저에는 지금까지의 모든 응답이 전달됩니다:

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
## 안내 메시지 (Informational Messages)

`note`, `info`, `warning`, `error`, `alert` 함수들을 이용해 다양한 안내 메시지를 표시할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 (Tables)

`table` 함수로 여러 행(row)과 컬럼(column) 형태의 데이터를 손쉽게 표시할 수 있습니다. 컬럼명과 데이터만 전달하면 됩니다:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀 (Spin)

`spin` 함수는 지정된 콜백이 실행되는 동안 스피너와 메시지를 표시합니다. 이는 작업이 진행 중임을 보여주며, 콜백의 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> `spin` 함수의 스피너 애니메이션을 사용하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다. 이 확장 모듈이 없으면 정적(이미지) 형태의 스피너만 표시됩니다.

<a name="progress"></a>
## 진행률 바 (Progress Bars)

소요 시간이 긴 작업은 얼마만큼 작업이 완료되었는지를 보여주는 진행률 바(progress bar)가 있으면 좋습니다. `progress` 함수를 사용하면, 주어진 iterable(반복 가능한 값)에 대해 각 반복마다 진행률 바가 자동으로 갱신됩니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 map 함수와 유사하게 동작하여, 콜백의 반환값을 모두 배열로 반환합니다.

콜백에서 `Laravel\Prompts\Progress` 인스턴스를 두 번째 인자로 받아 각 반복마다 라벨과 힌트를 동적으로 변경할 수도 있습니다:

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

진행률 바를 수동으로 제어해야 하는 경우, 총 단계 수를 정의한 뒤 각 아이템 처리 후 `advance` 메서드로 진행률을 수동 갱신하세요:

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
## 터미널 화면 지우기 (Clearing the Terminal)

`clear` 함수로 사용자의 터미널 화면을 지울 수 있습니다:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 관련 참고사항 (Terminal Considerations)

<a name="terminal-width"></a>
#### 터미널 너비

레이블, 옵션, 유효성 메시지의 길이가 터미널의 "컬럼 수"를 초과하면 자동으로 잘려서 표시됩니다. 사용자의 터미널이 좁을 수 있으므로, 메시지 길이는 가급적 짧게 유지하는 것이 좋습니다. 80자짜리 터미널을 지원하려면 길이 74자를 안전한 최대 길이로 삼으세요.

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인수를 받는 프롬프트의 경우, 사용자의 터미널 높이에 맞게 자동으로 표시 개수(행 수)가 제한됩니다. 유효성 메시지 공간도 포함됩니다.

<a name="fallbacks"></a>
## 지원되지 않는 환경 및 대체 동작 (Unsupported Environments and Fallbacks)

Laravel Prompts는 macOS, Linux, 그리고 WSL이 설치된 Windows를 지원합니다. Windows의 PHP 버전 한계 때문에, 지금은 WSL이 아닌 Windows 환경에선 사용할 수 없습니다.

이 때문에, Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html) 등의 대체 구현체로 자동 대체 동작을 지원합니다.

> [!NOTE]
> Laravel 프레임워크에서 Laravel Prompts를 사용할 때는 각 프롬프트에 대한 대체 동작이 자동으로 설정되어, 지원되지 않는 환경에서도 문제 없이 동작합니다.

<a name="fallback-conditions"></a>
#### 대체 동작 조건

Laravel이 아닌 환경이거나 직접 대체 동작 조건을 설정하고 싶다면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드로 Boolean을 전달하세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작 방식

Laravel이 아닌 환경이거나 개별 프롬프트 클래스의 대체 동작을 직접 커스터마이즈하고 싶다면, 각 프롬프트 클래스에 `fallbackUsing` 정적 메서드로 클로저를 등록하면 됩니다:

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

대체 동작은 프롬프트 클래스별로 각각 설정해야 하며, 클로저는 해당 프롬프트 인스턴스를 받아 적절한 타입의 값을 반환해야 합니다.

<a name="testing"></a>
## 테스트 (Testing)

Laravel에서는 명령에서 예상되는 Prompt 메시지가 제대로 표시되는지 테스트할 수 있는 다양한 메서드를 제공합니다:

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