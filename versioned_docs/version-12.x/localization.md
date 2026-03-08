# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [언어 파일 배포하기](#publishing-the-language-files)
    - [로케일 구성하기](#configuring-the-locale)
    - [복수형 언어 설정](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열 내 매개변수 치환하기](#replacing-parameters-in-translation-strings)
    - [복수형 처리하기](#pluralization)
- [패키지 언어 파일 덮어쓰기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로, Laravel 애플리케이션 골격에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자화하려면 `lang:publish` Artisan 명령어로 해당 파일들을 배포할 수 있습니다.

Laravel의 로컬라이제이션 기능은 다양한 언어의 문자열을 편리하게 가져올 수 있는 방법을 제공하여, 애플리케이션 내에서 다국어 지원을 쉽게 할 수 있게 합니다.

Laravel은 번역 문자열을 관리하는 두 가지 방식을 제공합니다. 첫 번째는 애플리케이션의 `lang` 디렉터리에 파일로 저장하는 방법입니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 존재할 수 있습니다. 이 방식은 Laravel에서 내장 기능(예: 유효성 검증 오류 메시지)의 번역 문자열을 관리할 때 주로 사용합니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또 다른 방식은 `lang` 디렉터리에 JSON 파일을 두고 번역 문자열을 정의하는 것입니다. 이 방법에서는 애플리케이션에서 지원하는 각 언어별로 대응하는 JSON 파일을 두게 됩니다. 번역 문자열이 많을 경우 이 방식을 권장합니다:

```text
/lang
    en.json
    es.json
```

이 문서에서는 두 가지 번역 문자열 관리 방식을 차례로 설명합니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 배포하기

기본적으로 Laravel 애플리케이션 골격에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel 언어 파일을 사용자화하거나 직접 생성하려면 `lang:publish` Artisan 명령어로 `lang` 디렉터리를 스캐폴딩하는 것이 좋습니다. 이 명령어는 애플리케이션에 `lang` 디렉터리를 생성하고 Laravel에서 사용하는 기본 언어 파일 세트를 배포합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 구성하기

애플리케이션의 기본 언어는 보통 `config/app.php` 설정 파일 내 `locale` 옵션에 저장되며, 이는 일반적으로 `APP_LOCALE` 환경 변수를 통해 설정됩니다. 필요에 따라 이 값을 자유롭게 변경할 수 있습니다.

또한, 기본 언어에 해당 번역이 없을 때 사용할 "대체 언어"도 설정할 수 있습니다. 대체 언어 역시 `config/app.php` 파일에서 설정되고, 보통 `APP_FALLBACK_LOCALE` 환경 변수로 값이 지정됩니다.

실행 중 단일 HTTP 요청에 대해 기본 언어를 변경하려면 `App` 파사드에서 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});
```

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

현재 로케일을 확인하거나 특정 로케일인지 확인할 때는 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어 설정

<div class="code-list-no-flex-break">

Eloquent와 프레임워크 일부에서 단수형 문자열을 복수형으로 변환하는 데 사용하는 Laravel의 "pluralizer"에 영어 외 다른 언어를 사용하도록 지시할 수 있습니다. 이 작업은 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 pluralizer가 지원하는 언어는 `french`(프랑스어), `norwegian-bokmal`(노르웨이어), `portuguese`(포르투갈어), `spanish`(스페인어), `turkish`(터키어)입니다.

</div>

```php
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}
```

> [!WARNING]
> pluralizer의 언어를 변경하는 경우, 반드시 Eloquent 모델의 [테이블 이름](/docs/12.x/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `lang` 디렉터리 내 파일에 저장합니다. 이 디렉터리 내부에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. 이 방식은 Laravel의 내장 기능(예: 유효성 검증 메시지) 번역 문자열 관리에 사용됩니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키-값 형태의 배열을 반환합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 지명이나 국가는 ISO 15897 표준에 따라 언어 디렉터리를 명명해야 합니다. 예를 들어 영국 영어는 "en_GB"로, "en-gb"가 아닙니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역 문자열이 매우 많아 짧은 키를 일일이 관리하기 어려운 경우, 번역 문자열 자체를 키로 쓰는 방법을 사용할 수 있습니다. 이 방식은 `lang` 디렉터리에 JSON 형식 파일로 정의하며, 예를 들어 스페인어를 지원한다면 `lang/es.json` 파일을 만듭니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키 / 파일명 충돌 주의사항

다른 번역 파일명과 충돌하는 키를 정의해서는 안 됩니다. 예를 들어 `__('Action')`을 "NL" 로케일에서 번역하려 할 때 `nl/action.php` 파일이 존재하고 `nl.json` 파일은 없으면, 해당 번역자는 `nl/action.php` 파일 전체를 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 헬퍼 함수를 이용해 언어 파일에서 번역 문자열을 가져올 수 있습니다. 짧은 키 방식을 사용할 경우, `.`(닷) 구문으로 파일명과 키를 함께 전달합니다. 예를 들어 `lang/en/messages.php` 파일 내 `welcome` 키 값을 가져올 때:

```php
echo __('messages.welcome');
```

만약 지정한 번역 문자열이 없으면 `__` 함수는 원래 키인 문자열을 그대로 반환합니다. 위 예시에서는 `messages.welcome`을 반환합니다.

[기본 번역 문자열을 키로 사용하는 방법](#using-translation-strings-as-keys)을 쓸 경우에는 `__` 함수에 해당 문자열의 기본 번역문을 그대로 넘깁니다:

```php
echo __('I love programming.');
```

없을 경우 역시 원래 문자열 자체를 반환합니다.

Blade 템플릿에서는 `{{ }}` 출력 구문을 활용할 수 있습니다:

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 매개변수 치환하기

필요한 경우 번역 문자열 내에 플레이스홀더(자리표시자)를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 이름을 넣는 환영 메시지를 정의할 수 있습니다:

```php
'welcome' => 'Welcome, :name',
```

번역 문자열을 가져올 때 치환할 값은 `__` 함수의 두 번째 인자로 배열 형태로 전달합니다:

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 전부 대문자거나 첫 글자만 대문자일 경우, 치환된 값도 대응되는 형식으로 자동 변환됩니다:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

번역 문자열 플레이스홀더에 객체를 사용할 경우, 해당 객체의 `__toString` 메서드가 호출됩니다. 이 메서드는 PHP의 내장 "매직 메서드" 중 하나입니다. 그러나 간혹 서드파티 라이브러리 클래스 등, `__toString` 메서드를 직접 제어하기 어려운 경우도 있습니다.

이때 Laravel에서는 특정 객체 유형에 대해 커스텀 포맷팅 핸들러를 등록할 수 있습니다. 이를 위해 번역자(translator)의 `stringable` 메서드를 호출하면 됩니다. `stringable` 메서드는 콜백을 받아, 이 콜백은 포맷팅 책임 객체 타입을 타입힌트로 명시해야 합니다. 보통 이 호출은 애플리케이션 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 수행합니다:

```php
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<a name="pluralization"></a>
### 복수형 처리하기

복수형 처리는 언어마다 다양한 복잡한 규칙이 있으므로 까다로운 문제이지만, Laravel은 사용자가 정의한 복수형 규칙에 따라 다르게 번역할 수 있게 도와줍니다. `|` 문자로 단수형과 복수형 구분이 가능합니다:

```php
'apples' => 'There is one apple|There are many apples',
```

물론 [번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)에서도 복수형을 지원합니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

더욱 복잡한 복수형 규칙도 만들 수 있습니다. 예를 들어, 여러 개수 구간별 메시지를 지정할 수 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 옵션이 포함된 번역 문자열을 정의한 뒤에는 `trans_choice` 함수를 사용해 주어진 "개수"에 맞는 문장 형태를 가져옵니다. 아래 예에서는 1보다 크므로 복수형 번역 문자열이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);
```

복수형 문자열 안에 플레이스홀더도 정의할 수 있으며, 이는 `trans_choice` 함수의 세 번째 인자로 배열로 전달해 치환할 수 있습니다:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 전달한 정수 값을 표시하고 싶을 때는 내장 플레이스홀더인 `:count`를 사용할 수 있습니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 덮어쓰기

일부 패키지는 자체 언어 파일을 포함하여 배포합니다. 패키지 코어 파일을 직접 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 두어 번역 문자열을 덮어쓸 수 있습니다.

예를 들어 `skyrim/hearthfire`라는 패키지의 영어 `messages.php` 번역 문자열을 덮어쓰려면, `lang/vendor/hearthfire/en/messages.php` 경로에 파일을 두면 됩니다. 이 파일에는 덮어쓸 번역 문자열만 정의하면 되며, 수정하지 않은 문자열은 원래 패키지 언어 파일에서 계속 로드됩니다.