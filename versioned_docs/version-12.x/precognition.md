# Precognition (Precognition)

- [소개](#introduction)
- [라이브 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [React 사용하기](#using-react)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [배열 유효성 검증](#validating-arrays)
- [유효성 검증 규칙 커스터마이즈](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래의 HTTP 요청 결과를 예측할 수 있도록 해줍니다. Precognition의 주요 활용 사례 중 하나는, 프론트엔드 JavaScript 애플리케이션에서 "라이브" 유효성 검증(live validation)을 제공할 수 있다는 점입니다. 이로 인해 백엔드 유효성 검증 규칙을 프론트엔드에 중복해서 구현할 필요가 없습니다.

Laravel이 "precognitive request"를 받으면, 해당 라우트의 모든 미들웨어를 실행하고 컨트롤러의 의존성(유효성 검증이 포함된 [폼 리퀘스트](/docs/12.x/validation#form-request-validation))을 해결합니다. 하지만 실제 컨트롤러 메서드는 실행하지 않습니다.

> [!NOTE]
> Inertia 2.3부터 Precognition이 내장 지원됩니다. 자세한 내용은 [Inertia Forms 문서](https://inertiajs.com/docs/v2/the-basics/forms)를 참고하세요. 더 이전 버전의 Inertia는 Precognition 0.x가 필요합니다.

<a name="live-validation"></a>
## 라이브 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면, 프론트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복하지 않고도 사용자에게 라이브 유효성 검증 경험을 제공할 수 있습니다. 작동 방식을 보여주기 위해, 새로운 사용자를 생성하는 폼을 예제로 만들어 보겠습니다.

먼저, Precognition을 라우트에서 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 그리고 해당 라우트의 유효성 검증 규칙을 담을 [폼 리퀘스트](/docs/12.x/validation#form-request-validation) 클래스를 생성하세요.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, 프론트엔드에서 Vue용 Laravel Precognition 헬퍼를 NPM으로 설치합니다.

```shell
npm install laravel-precognition-vue
```

이제 Precognition 패키지를 설치했다면, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성할 수 있습니다. 여기에는 HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터가 필요합니다.

라이브 유효성 검증을 활성화하려면, `change` 이벤트에서 해당 input의 이름과 함께 폼의 `validate` 메서드를 호출하면 됩니다.

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

이제 사용자가 폼을 입력할 때 Precognition이 라우트의 폼 리퀘스트에 정의된 유효성 검증 규칙을 기반으로 라이브 유효성 검증 결과를 제공합니다. 입력값이 변경되면 디바운스된 "precognitive" 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 대기 시간을 `setValidationTimeout` 함수로 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 땐, `validating` 속성이 `true`가 됩니다.

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검증 중 혹은 폼 제출 시 반환된 오류는 자동으로 `errors` 객체에 채워집니다.

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 존재하는지 확인하고 싶다면 `hasErrors` 속성을 사용하세요.

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

개별 input이 유효한지 또는 무효한지 확인하고 싶을 때는, 해당 input 이름을 `valid` 또는 `invalid` 함수에 각각 전달하세요.

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 input의 값이 변경되고 유효성 검증 응답을 받을 때에만 해당 input이 유효(valid) 또는 무효(invalid)로 표시됩니다.

Precognition으로 폼의 일부 필드만 검증하고 있다면, 오류를 직접 지워야 할 때가 있습니다. 이럴 때는 `forgetError` 함수를 사용할 수 있습니다.

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

이처럼 사용자의 input 이벤트(change)에 후킹해 개별 input을 검증할 수 있습니다. 하지만, 사용자가 아직 조작하지 않은 항목까지 한 번에 검증해야 하는 경우도 있습니다. 대표적으로 "위저드" 인터페이스에서, 다음 단계로 넘어가기 전 모든 표시된 input을 검증해야 할 경우입니다.

이럴 때는, `validate` 메서드에 검증이 필요한 필드 이름을 `only` 옵션으로 전달하면 됩니다. 그리고 검증 성공 또는 검증 오류에 대한 처리를 각각 `onSuccess`, `onValidationError` 콜백에서 할 수 있습니다.

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

물론, 폼 제출(response)에 대한 처리가 필요하다면, `submit` 함수는 Axios 요청 프라미스를 반환하므로, 이를 이용해 응답 데이터 접근, 폼 초기화, 오류 처리 등을 할 수 있습니다.

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

폼이 전송되는 중인지 확인하려면 `processing` 속성을 확인하세요.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-react"></a>
### React 사용하기

Laravel Precognition을 이용하면, 프론트엔드 React 애플리케이션에서도 유효성 검증 규칙을 중복할 필요 없이 라이브 유효성 검증을 구현할 수 있습니다. 새로운 사용자를 생성하는 폼 예제로 살펴보겠습니다.

먼저, Precognition을 라우트에서 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하고, 유효성 검증 규칙을 정의하는 [폼 리퀘스트](/docs/12.x/validation#form-request-validation)를 생성하세요.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, React용 Laravel Precognition 헬퍼를 NPM으로 설치하세요.

```shell
npm install laravel-precognition-react
```

Precognition 패키지 설치 후에는, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터를 전달합니다.

라이브 유효성 검증을 활성화하려면, 각 input의 `change`와 `blur` 이벤트를 리스닝해야 합니다. `change` 핸들러에서는 `setData`로 폼 데이터를 업데이트하고, `blur` 핸들러에서 `validate`를 호출하면 됩니다.

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

이제 사용자 입력이 들어올 때 Precognition이 라우트의 폼 리퀘스트에 정의된 유효성 검증을 실시간으로 수행합니다. 입력값이 변경될 때마다 디바운스된 precognitive 유효성 검증 요청이 Laravel로 전송됩니다. 디바운스 대기 시간은 `setValidationTimeout` 함수로 조절할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청 중일 때는, `validating` 속성이 `true`가 됩니다.

```jsx
{form.validating && <div>Validating...</div>}
```

검증 오류가 반환될 경우, 해당 오류는 자동으로 폼의 `errors` 객체에 채워집니다.

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 판단하려면 `hasErrors` 속성을 사용하세요.

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

특정 input에 대해 검증 결과가 유효 또는 무효인지, 각각 `valid`와 `invalid` 함수로 확인할 수 있습니다.

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> input이 변경되고 유효성 응답이 올 때에만 유효 또는 무효로 표시됩니다.

Precognition으로 폼의 일부 input만 검증하고 있다면, 오류를 수동으로 지울 수 있는데, `forgetError` 함수를 사용하세요.

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.files[0]);

        form.forgetError('avatar');
    }}
>
```

이처럼 input의 `blur` 이벤트 등을 활용해 개별 input을 검증할 수 있습니다. 하지만, 아직 사용자가 입력하지 않은 필드도 검증해야 하는 시나리오, 예를 들어 "위저드"에서 모든 표시된 필드를 검증해야 하는 상황도 있습니다.

이럴 때는 `validate` 메서드의 `only` 옵션에 필드명을 배열로 전달하고, 결과 처리를 `onSuccess`, `onValidationError` 콜백에서 할 수 있습니다.

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

또한, 폼 제출 후 결과에 따라 코드 실행이 필요하다면, `submit` 함수가 Axios 요청 프라미스를 반환하므로 이를 활용해 응답 처리, 폼 초기화, 실패 처리 등이 가능합니다.

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

폼 전송이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다.

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-alpine"></a>
### Alpine과 Blade 사용하기

Laravel Precognition을 활용하면, Alpine 기반의 프론트엔드 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 라이브 유효성 검증을 구현할 수 있습니다. 아래는 사용자 생성 폼을 예시로 설명합니다.

먼저 Precognition을 라우트에서 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하고, 검증 규칙을 담은 [폼 리퀘스트](/docs/12.x/validation#form-request-validation)를 생성해야 합니다.

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

이후, Alpine용 Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다.

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 Precognition 플러그인을 Alpine에 등록합니다.

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Precognition 패키지 설치와 등록이 끝났다면, `$form` "매직"을 이용해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터를 넘겨줍니다.

라이브 유효성 검증을 적용하려면, 폼의 데이터를 각 input에 바인딩하고, 각 input의 `change` 이벤트에서 `validate` 메서드를 호출해야 합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

이제 폼이 입력될 때 Precognition이 라우트의 폼 리퀘스트에 정의된 유효성 검증으로 실시간 피드백을 제공합니다. 입력값이 변경될 때마다 디바운스된 검증 요청이 Laravel로 전송됩니다. 대기 시간은 `setValidationTimeout` 함수로 조절 가능합니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청 중일 때는 `validating` 속성이 `true`가 됩니다.

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

유효성 검증 오류는 자동으로 `errors` 객체에 반영됩니다.

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼 전체에 오류가 있는지 `hasErrors` 속성으로 체크할 수 있습니다.

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

input의 검증 성공 또는 실패 여부는 각각 `valid`, `invalid` 함수를 이용해 확인합니다.

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> input이 변경되고 유효성 검증 응답이 반환되어야만 유효 또는 무효로 표시됩니다.

이처럼 input의 `change` 이벤트로 실시간 검증이 가능하지만, 아직 손대지 않은 input까지 포함해 전체 검증이 필요할 때(예: 위저드에서 다음 단계로 이동 전), `validate` 메서드에서 검증할 필드명을 `only` 옵션에 배열로 넘기고, 결과는 `onSuccess`, `onValidationError` 콜백으로 처리할 수 있습니다.

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

폼 제출 요청 중 여부는 `processing` 속성으로 확인합니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 자동 채우기 (Repopulating Old Form Data)

위의 사용자 등록 예제에서는 Precognition으로 라이브 유효성 검증만 사용하고 폼 제출은 전통적인 서버 사이드 제출로 처리하고 있습니다. 그래서, 제출 오류가 발생하면 기존 입력값(`old input`)과 서버에서 반환된 유효성 검증 오류를 폼에 채워주어야 합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

반대로, 폼 제출을 XHR로 처리하려면 `submit` 함수를 사용하면 됩니다. 이 함수는 Axios 요청 프라미스를 반환합니다.

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    this.form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Axios 설정하기 (Configuring Axios)

Precognition의 라이브러리들은 HTTP 요청을 애플리케이션 백엔드에 전송할 때 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용합니다. 필요하다면 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때는 `resources/js/app.js`에서 각 요청에 추가 헤더를 지정할 수 있습니다.

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

또는 이미 커스터마이징된 Axios 인스턴스가 있다면, Precognition에 해당 인스턴스를 사용하도록 설정할 수도 있습니다.

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

<a name="validating-arrays"></a>
## 배열 유효성 검증 (Validating Arrays)

배열이나 중첩 객체 내의 필드를 검증해야 할 때, 와일드카드(*)를 사용할 수 있습니다. 각각의 `*`는 경로 세그먼트 하나를 의미합니다.

```js
// 배열 내 모든 사용자 email을 검증...
form.validate('users.*.email');

// profile 객체의 모든 필드를 검증...
form.validate('profile.*');

// 모든 사용자에 대한 모든 필드 검증...
form.validate('users.*.*');
```

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이즈 (Customizing Validation Rules)

precognitive 요청이 올 때, `isPrecognitive` 메서드를 활용해 유효성 검증 규칙을 커스터마이즈할 수 있습니다.

예를 들어, 사용자 등록 폼에서는 최종 제출 시에만 비밀번호의 "uncompromised(유출되지 않았는지)" 검증을 하고 싶고, precognitive 요청에는 필수 및 최소 길이 확인만 하고 싶을 때, `isPrecognitive`를 활용해 폼 리퀘스트의 규칙을 다음과 같이 변경할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * 유효성 검증 규칙을 반환합니다.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-file-uploads"></a>
## 파일 업로드 처리 (Handling File Uploads)

기본적으로 Precognition은 precognitive 유효성 검증 요청 시 파일을 업로드하거나 검증하지 않습니다. 이로 인해 큰 파일이 불필요하게 여러 번 업로드되는 것을 방지할 수 있습니다.

따라서, [해당 폼 리퀘스트의 유효성 검증 규칙을 커스터마이즈](#customizing-validation-rules)하여 파일 필드는 전체 폼 제출시에만 필수로 처리되도록 해야 합니다.

```php
/**
 * 유효성 검증 규칙을 반환합니다.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

모든 유효성 검증 요청마다 파일을 포함시키고 싶다면, 클라이언트 측 폼 인스턴스에서 `validateFiles` 함수를 호출하면 됩니다.

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수효과 관리 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, precognitive 요청 중에는 건너뛰는 것이 적절한 부수효과(사이드이펙트)를 발생시키는 다른 미들웨어가 있는지 반드시 고려해야 합니다.

예를 들어, 사용자가 애플리케이션과 상호작용할 때마다 총 "상호작용(interaction)" 개수를 증가시키는 미들웨어가 있는데, precognitive 요청은 상호작용 횟수에 포함하고 싶지 않은 경우가 있을 수 있습니다. 이런 상황에서는 상호작용 카운트 전에 요청의 `isPrecognitive` 여부를 체크하면 됩니다.

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트에서 precognitive 요청을 보내려면, Laravel의 `TestCase`에서 제공하는 `withPrecognition` 헬퍼를 사용하면 됩니다. 이 헬퍼는 `Precognition` 요청 헤더를 추가합니다.

또한 precognitive 요청이 성공적으로 처리되었는지(즉, 유효성 검증 에러가 없는지) 확인하려면, 응답 객체의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다.

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```