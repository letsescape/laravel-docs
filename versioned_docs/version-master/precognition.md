# 프리코그니션 (Precognition)

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [React 사용하기](#using-react)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [배열 유효성 검증](#validating-arrays)
- [유효성 검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부작용 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 향후 HTTP 요청의 결과를 미리 예측(anticipate)할 수 있도록 해줍니다. Precognition의 주요 활용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드의 유효성 검증(validation) 규칙을 중복 작성할 필요 없이 "실시간" 유효성 검증 기능을 제공하는 것입니다.

Laravel이 "프리코그니션 요청(precognitive request)"을 수신하면, 해당 라우트의 모든 미들웨어를 실행하고 컨트롤러의 의존성도 해석(의존성 주입 포함)하며, [폼 요청](/docs/master/validation#form-request-validation) 유효성 검증 절차도 처리합니다. 하지만 컨트롤러 메서드는 실제로 실행하지 않습니다.

> [!NOTE]
> Inertia 2.3부터 Precognition 지원이 내장되어 있습니다. 자세한 내용은 [Inertia Forms 문서](https://inertiajs.com/docs/v2/the-basics/forms)를 참고하십시오. 이전 버전의 Inertia에서는 Precognition 0.x가 필요합니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면, 프론트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복 구현하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 예시로, 새로운 사용자를 생성하는 폼을 만들어봅니다.

먼저 Precognition을 활성화하려면 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 또, 라우트의 유효성 검증 규칙을 정의할 [폼 요청](/docs/master/validation#form-request-validation) 클래스를 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 NPM을 통해 Vue용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다.

```shell
npm install laravel-precognition-vue
```

Laravel Precognition 패키지를 설치했다면, 이제 Precognition의 `useForm` 함수를 사용하여 폼 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 요청 URL(`/users`), 초기 폼 데이터를 전달합니다.

그리고, 입력값마다 `change` 이벤트에서 폼의 `validate` 메서드를 호출하여 실시간 유효성 검증을 활성화할 수 있습니다(입력 이름을 인수로 전달).

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

이제 사용자가 폼을 입력하면, Precognition이 라우트의 폼 요청에 정의된 유효성 검증 규칙에 따라 실시간으로 검증 결과를 제공합니다. 입력값이 변경될 때마다 디바운스(debounce)된 "프리코그니션" 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 시간은 `setValidationTimeout` 함수로 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

검증 요청이 처리 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```html
<div v-if="form.validating">
    Validating...
</div>
```

검증 요청이나 폼 제출 중에 반환된 유효성 검증 에러는, 폼의 `errors` 객체에 자동으로 저장됩니다.

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 에러가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다.

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

또한, 각 입력값이 유효(valid) 또는 무효(invalid)인지 여부를 폼의 `valid` 및 `invalid` 함수에 입력 이름을 전달해서 확인할 수 있습니다.

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 각 폼 입력값은 변경되고 나서, 그리고 검증 응답을 받은 이후에만 유효 또는 무효 상태로 표시됩니다.

Precognition으로 폼의 일부 입력만 검증할 때는 필요에 따라 에러 정보를 수동으로 지울 수 있습니다. 이를 위해 폼의 `forgetError` 함수를 사용합니다.

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

앞서 본 것처럼 입력값의 `change` 이벤트에서 검증을 수행할 수 있지만, 사용자가 아직 상호작용하지 않은 입력값까지 한 번에 검증해야 할 수도 있습니다. (예: "다음 단계"로 진행하기 전에 모든 보이는 입력값을 검증하는 "마법사" UI)  
이때는 `validate` 메서드를 호출할 때 `only` 설정 키로 검증할 필드명을 배열로 전달할 수 있습니다. 응답에 따라 `onSuccess`, `onValidationError` 콜백도 지정할 수 있습니다.

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

물론 폼 제출 응답에 따라 추가적인 처리를 할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청을 반환하므로, 응답 데이터에 접근하거나 성공 시 입력값을 리셋(reset)하거나 실패 시 에러 처리를 할 때 적합합니다.

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

폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-react"></a>
### React 사용하기

Laravel Precognition을 사용하면, 프론트엔드 React 애플리케이션에서도 백엔드 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증 기능을 제공할 수 있습니다. 새로운 사용자 생성 폼 예시로 설명합니다.

우선 Precognition 활성화를 위해 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 유효성 검증 규칙을 위한 [폼 요청](/docs/master/validation#form-request-validation) 클래스를 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, React 버전의 Laravel Precognition 프론트엔드 헬퍼를 NPM을 통해 설치합니다.

```shell
npm install laravel-precognition-react
```

Laravel Precognition 패키지를 설치했다면, Precognition의 `useForm` 함수를 사용하여 폼 객체를 만듭니다. HTTP 메서드(`post`), URL(`/users`), 초기 데이터 등을 전달합니다.

실시간 검증을 위해 각 입력값의 `change` 및 `blur` 이벤트에 반응해야 합니다.  
- `change` 이벤트에서는 `setData` 함수로 입력값을 저장  
- `blur` 이벤트에서는 `validate` 함수를 호출하며 입력 이름을 전달합니다.

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

이제 사용자가 폼을 입력하면 Precognition이 라우트 폼 요청의 유효성 검증 규칙에 따라 실시간으로 결과를 제공합니다. 입력값 변경 시 디바운스된 "프리코그니션" 검증 요청이 전송됩니다.  
디바운스 시간은 `setValidationTimeout` 함수로 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

검증 요청이 처리 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```jsx
{form.validating && <div>Validating...</div>}
```

검증 요청이나 폼 제출 중 반환된 유효성 검증 에러는 폼의 `errors` 객체에 자동으로 저장됩니다.

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 에러가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다.

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

각 입력이 유효(valid) 또는 무효(invalid)인지 여부를 `valid`, `invalid` 함수에 입력 이름을 전달해 확인할 수 있습니다.

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력값이 변경되고 검증 응답을 받은 이후에만 유효 또는 무효로 표시됩니다.

Precognition으로 폼 일부 입력만 검증할 때는 에러 정보를 수동으로 삭제할 수 있습니다. 이를 위해 `forgetError` 함수를 사용합니다.

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

입력값의 `blur` 이벤트에서 개별 검증도 가능하지만, 사용자가 미처 건드리지 않은 입력까지 한 번에 검증이 필요할 때가 있습니다(예: 마법사 형태 UI).  
이때는 `validate` 호출 시 `only` 설정에 필드명 배열을 전달하고, 결과에 따라 `onSuccess`, `onValidationError` 콜백을 지정할 수 있습니다.

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

물론, 폼 제출 응답에 따라 추가 처리가 필요하다면 폼의 `submit` 함수가 반환하는 Axios 프로미스에서 처리하면 됩니다.

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

폼 제출이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다.

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-alpine"></a>
### Alpine과 Blade 사용하기

Laravel Precognition을 이용하면 Alpine 기반 프론트엔드에서도 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증 경험을 제공할 수 있습니다. 역시 새로운 사용자 생성 폼 예시로 설명합니다.

먼저 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 유효성 검증 규칙을 가진 [폼 요청](/docs/master/validation#form-request-validation) 클래스를 작성합니다.

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

NPM을 이용해 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다.

```shell
npm install laravel-precognition-alpine
```

그 다음, `resources/js/app.js` 파일에서 Precognition 플러그인을 Alpine에 등록합니다.

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Precognition 패키지 설치 및 등록이 완료되면, Alpine의 `$form` "magic"을 사용해 폼 객체를 만들 수 있습니다. HTTP 메서드(`post`), URL(`/users`), 초기 데이터를 지정하세요.

실시간 검증을 위해 입력값 각각에 x-model로 폼 데이터를 바인딩하고, 입력값의 `change` 이벤트에서 `validate` 메서드를 호출합니다.

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

이제 사용자가 폼을 채워가면 Precognition이 폼 요청의 검증 규칙에 따라 실시간 유효성 검증 결과를 제공합니다. 입력이 바뀔 때마다 디바운스된 검증 요청이 서버로 전송됩니다. 디바운스 시간은 `setValidationTimeout` 함수로 설정 가능합니다.

```js
form.setValidationTimeout(3000);
```

검증 요청 처리 중에는 `validating` 속성으로 상태를 확인할 수 있습니다.

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

에러는 폼의 `errors` 객체에 자동으로 채워집니다.

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 에러가 있는지 `hasErrors` 속성으로 확인 가능합니다.

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

입력이 유효/무효한지 `valid`, `invalid` 함수로 상태를 표시할 수 있습니다.

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력값은 변경 후, 그리고 검증 응답을 받은 다음에만 유효 또는 무효로 나타납니다.

앞서 살펴본 것처럼 입력의 `change` 이벤트에 걸어서 검증을 할 수 있지만, 미처 건드리지 않은 입력까지 한 번에 검증해야 하는 경우도 많습니다(주로 마법사 UI).  
이때는 `validate` 호출 시 `only` 키에 검증할 필드명을 배열로 전달하고, `onSuccess`, `onValidationError` 핸들러로 응답을 처리하세요.

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

폼 제출 요청이 진행 중인지 `processing` 속성으로 확인할 수 있습니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 입력값 복원

위에 예시로 든 사용자 생성 폼에서는 Precognition으로 실시간 검증을 하고 있지만, 최종 제출은 서버 사이드 폼 제출 방식입니다. 이 경우 서버가 반환한 "이전 입력값(old input)"과 유효성 검증 에러로 폼을 초기화해야 합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

만약 폼을 XHR로 제출하고 싶다면 폼의 `submit` 함수를 사용할 수 있습니다. 이 함수는 Axios 요청 프로미스를 반환합니다.

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
### Axios 설정하기

Precognition 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 이용해 백엔드로 요청을 전송합니다. 필요시, Axios 인스턴스를 커스터마이징할 수 있습니다.  
예를 들어, `laravel-precognition-vue`를 사용할 때 `resources/js/app.js` 파일에서 모든 요청에 추가 헤더를 첨부할 수 있습니다.

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 애플리케이션을 위한 Axios 인스턴스가 있다면 Precognition이 그 인스턴스를 사용하도록 지정할 수도 있습니다.

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

<a name="validating-arrays"></a>
## 배열 유효성 검증 (Validating Arrays)

배열이나 중첩 객체 내의 필드를 검증할 때 와일드카드 `*`을 사용할 수 있습니다. 각 `*`는 경로의 한 구간(segment)에 매칭됩니다.

```js
// 배열 내 모든 사용자에 대해 email 검증
form.validate('users.*.email');

// profile 객체 내의 모든 필드 검증
form.validate('profile.*');

// 모든 사용자, 모든 필드 검증
form.validate('users.*.*');
```

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이징 (Customizing Validation Rules)

`isPrecognitive` 메서드를 사용하면 프리코그니션 요청 시 실행되는 유효성 검증 규칙을 커스터마이징할 수 있습니다.

예를 들어, 사용자 생성 폼에서는 실제 폼 제출 시에만 비밀번호가 "유출되지 않았는지(uncompromised)" 검증하고, 프리코그니션 검증 요청에서는 단순히 비밀번호 필수 및 최소 길이만 검사하도록 구현할 수 있습니다.  
아래처럼 `isPrecognitive` 메서드를 이용해 폼 요청 내에서 검증 규칙을 동적으로 지정할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
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

기본적으로 Laravel Precognition은 프리코그니션 유효성 검증 요청에서는 파일을 업로드하거나 검증하지 않습니다. 이렇게 하면 대용량 파일이 불필요하게 여러 번 업로드되는 일을 막을 수 있습니다.

이러한 동작 때문에 [해당 폼 요청의 검증 규칙을 커스터마이징](#customizing-validation-rules)하여, 파일 필드는 전체 폼 제출시에만 필수로 하도록 처리해야 합니다.

```php
/**
 * Get the validation rules that apply to the request.
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

모든 검증 요청마다 파일도 포함시키고 싶다면, 클라이언트 사이드 폼 인스턴스에서 `validateFiles` 함수를 호출할 수 있습니다.

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부작용 관리 (Managing Side-Effects)

라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때, 프리코그니션 요청 동안 _다른_ 미들웨어에서 발생하는 부작용(side-effect)을 건너뛰어야 하는지 고려해야 합니다.

예를 들어, 사용자가 애플리케이션과 상호작용(interaction)을 할 때마다 횟수를 증가시키는 미들웨어가 있다고 가정합시다. 프리코그니션 요청에 대해서는 상호작용 횟수를 증가시키고 싶지 않을 수 있습니다.  
이럴 때, 미들웨어 내에서 `$request->isPrecognitive()` 메서드를 활용해 프리코그니션 요청이면 카운트 증가를 건너뛸 수 있습니다.

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

테스트에서 프리코그니션 요청을 만들고 싶을 때, Laravel의 `TestCase`에 내장된 `withPrecognition` 헬퍼를 사용할 수 있습니다. 이 헬퍼는 `Precognition` 요청 헤더를 추가합니다.

추가로, 프리코그니션 요청이 성공적(즉, 유효성 검증 에러가 없었는지)인지 단언(assert)하려면 응답 객체의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다.

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