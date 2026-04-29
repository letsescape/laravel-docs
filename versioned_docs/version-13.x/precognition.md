# Precognition (Precognition)

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [React 사용하기](#using-react)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [배열 유효성 검증](#validating-arrays)
- [유효성 검증 규칙 사용자 정의](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition을 사용하면 앞으로 실행될 HTTP 요청의 결과를 미리 예상할 수 있습니다. Precognition의 주요 사용 사례 중 하나는 애플리케이션의 백엔드 유효성 검증 규칙을 프론트엔드 JavaScript 애플리케이션에 중복해서 작성하지 않고도 "실시간" 유효성 검증을 제공하는 것입니다.

Laravel이 "precognitive request"를 받으면 라우트의 모든 Middleware를 실행하고, [form requests](/docs/13.x/validation#form-request-validation) 유효성 검증을 포함해 라우트 컨트롤러의 의존성을 resolve합니다. 하지만 실제로 라우트의 컨트롤러 메서드를 실행하지는 않습니다.

> [!NOTE]
> Inertia 2.3부터 Precognition 지원이 내장되어 있습니다. 자세한 내용은 [Inertia Forms 문서](https://inertiajs.com/forms)를 참고하십시오. 이전 Inertia 버전에서는 Precognition 0.x가 필요합니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면 프론트엔드 Vue 애플리케이션에 유효성 검증 규칙을 중복해서 작성하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 동작 방식을 살펴보기 위해 애플리케이션에서 새 사용자를 생성하는 form을 만들어 보겠습니다.

먼저 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` Middleware를 라우트 정의에 추가해야 합니다. 또한 라우트의 유효성 검증 규칙을 담을 [form request](/docs/13.x/validation#form-request-validation)도 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 NPM을 통해 Vue용 Laravel Precognition 프론트엔드 헬퍼를 설치해야 합니다.

```shell
npm install laravel-precognition-vue
```

Laravel Precognition 패키지를 설치했으면 이제 Precognition의 `useForm` 함수를 사용해 form 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 form 데이터를 제공합니다.

그런 다음 실시간 유효성 검증을 활성화하려면 각 입력의 `change` 이벤트에서 form의 `validate` 메서드를 호출하고, 입력의 이름을 전달합니다.

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

이제 사용자가 form을 채워 나가면 Precognition은 라우트의 form request에 정의된 유효성 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. form의 입력이 변경되면 debounce 처리된 "precognitive" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. form의 `setValidationTimeout` 함수를 호출해 debounce 제한 시간을 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면 form의 `validating` 속성이 `true`가 됩니다.

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검증 요청 또는 form 제출 중 반환된 모든 유효성 검증 오류는 form의 `errors` 객체에 자동으로 채워집니다.

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

form에 오류가 있는지 여부는 form의 `hasErrors` 속성으로 확인할 수 있습니다.

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

또한 입력의 이름을 form의 `valid` 및 `invalid` 함수에 각각 전달하여, 해당 입력이 유효성 검증을 통과했는지 또는 실패했는지 확인할 수 있습니다.

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> form 입력은 변경된 뒤 유효성 검증 응답을 받은 후에만 유효 또는 유효하지 않음으로 표시됩니다.

Precognition으로 form 입력의 일부만 유효성 검증하는 경우, 오류를 수동으로 지우는 것이 유용할 수 있습니다. 이를 위해 form의 `forgetError` 함수를 사용할 수 있습니다.

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

앞에서 살펴본 것처럼 입력의 `change` 이벤트에 연결하여 사용자가 입력과 상호작용할 때 개별 입력을 유효성 검증할 수 있습니다. 하지만 사용자가 아직 상호작용하지 않은 입력도 유효성 검증해야 할 수 있습니다. 예를 들어 "wizard"를 만들 때 다음 단계로 이동하기 전에, 사용자가 상호작용했는지 여부와 관계없이 현재 보이는 모든 입력을 유효성 검증하고 싶을 때가 흔합니다.

Precognition으로 이를 처리하려면 `validate` 메서드를 호출하면서 유효성 검증하려는 필드 이름을 `only` 설정 키에 전달해야 합니다. 유효성 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다.

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

물론 form 제출에 대한 응답에 반응하여 코드를 실행할 수도 있습니다. form의 `submit` 함수는 Axios 요청 promise를 반환합니다. 이를 통해 응답 payload에 접근하거나, 제출 성공 시 form 입력을 초기화하거나, 실패한 요청을 처리할 수 있습니다.

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

form 제출 요청이 진행 중인지 여부는 form의 `processing` 속성을 확인하여 알 수 있습니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-react"></a>
### React 사용하기

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에 유효성 검증 규칙을 중복해서 작성하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 동작 방식을 살펴보기 위해 애플리케이션에서 새 사용자를 생성하는 form을 만들어 보겠습니다.

먼저 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` Middleware를 라우트 정의에 추가해야 합니다. 또한 라우트의 유효성 검증 규칙을 담을 [form request](/docs/13.x/validation#form-request-validation)도 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 NPM을 통해 React용 Laravel Precognition 프론트엔드 헬퍼를 설치해야 합니다.

```shell
npm install laravel-precognition-react
```

Laravel Precognition 패키지를 설치했으면 이제 Precognition의 `useForm` 함수를 사용해 form 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 form 데이터를 제공합니다.

실시간 유효성 검증을 활성화하려면 각 입력의 `change` 및 `blur` 이벤트를 감지해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수를 사용해 입력의 이름과 새 값을 전달하여 form 데이터를 설정해야 합니다. 그런 다음 `blur` 이벤트 핸들러에서 form의 `validate` 메서드를 호출하고 입력의 이름을 전달합니다.

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

이제 사용자가 form을 채워 나가면 Precognition은 라우트의 form request에 정의된 유효성 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. form의 입력이 변경되면 debounce 처리된 "precognitive" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. form의 `setValidationTimeout` 함수를 호출해 debounce 제한 시간을 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면 form의 `validating` 속성이 `true`가 됩니다.

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 검증 요청 또는 form 제출 중 반환된 모든 유효성 검증 오류는 form의 `errors` 객체에 자동으로 채워집니다.

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

form에 오류가 있는지 여부는 form의 `hasErrors` 속성으로 확인할 수 있습니다.

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

또한 입력의 이름을 form의 `valid` 및 `invalid` 함수에 각각 전달하여, 해당 입력이 유효성 검증을 통과했는지 또는 실패했는지 확인할 수 있습니다.

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> form 입력은 변경된 뒤 유효성 검증 응답을 받은 후에만 유효 또는 유효하지 않음으로 표시됩니다.

Precognition으로 form 입력의 일부만 유효성 검증하는 경우, 오류를 수동으로 지우는 것이 유용할 수 있습니다. 이를 위해 form의 `forgetError` 함수를 사용할 수 있습니다.

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

앞에서 살펴본 것처럼 입력의 `blur` 이벤트에 연결하여 사용자가 입력과 상호작용할 때 개별 입력을 유효성 검증할 수 있습니다. 하지만 사용자가 아직 상호작용하지 않은 입력도 유효성 검증해야 할 수 있습니다. 예를 들어 "wizard"를 만들 때 다음 단계로 이동하기 전에, 사용자가 상호작용했는지 여부와 관계없이 현재 보이는 모든 입력을 유효성 검증하고 싶을 때가 흔합니다.

Precognition으로 이를 처리하려면 `validate` 메서드를 호출하면서 유효성 검증하려는 필드 이름을 `only` 설정 키에 전달해야 합니다. 유효성 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다.

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

물론 form 제출에 대한 응답에 반응하여 코드를 실행할 수도 있습니다. form의 `submit` 함수는 Axios 요청 promise를 반환합니다. 이를 통해 응답 payload에 접근하거나, form 제출 성공 시 form 입력을 초기화하거나, 실패한 요청을 처리할 수 있습니다.

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

form 제출 요청이 진행 중인지 여부는 form의 `processing` 속성을 확인하여 알 수 있습니다.

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-alpine"></a>
### Alpine과 Blade 사용하기

Laravel Precognition을 사용하면 프론트엔드 Alpine 애플리케이션에 유효성 검증 규칙을 중복해서 작성하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 동작 방식을 살펴보기 위해 애플리케이션에서 새 사용자를 생성하는 form을 만들어 보겠습니다.

먼저 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` Middleware를 라우트 정의에 추가해야 합니다. 또한 라우트의 유효성 검증 규칙을 담을 [form request](/docs/13.x/validation#form-request-validation)도 생성해야 합니다.

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 NPM을 통해 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 설치해야 합니다.

```shell
npm install laravel-precognition-alpine
```

그런 다음 `resources/js/app.js` 파일에서 Precognition 플러그인을 Alpine에 등록합니다.

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Laravel Precognition 패키지를 설치하고 등록했으면 이제 Precognition의 `$form` "magic"을 사용해 form 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 form 데이터를 제공합니다.

실시간 유효성 검증을 활성화하려면 form의 데이터를 관련 입력에 바인딩한 다음, 각 입력의 `change` 이벤트를 감지해야 합니다. `change` 이벤트 핸들러에서는 form의 `validate` 메서드를 호출하고 입력의 이름을 전달해야 합니다.

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
이제 사용자가 폼을 입력하면 Precognition은 라우트의 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. 폼 입력값이 변경되면 디바운스된 "precognitive" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 폼의 `setValidationTimeout` 함수를 호출하여 디바운스 대기 시간을 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

유효성 검증 요청 또는 폼 제출 중 반환된 모든 유효성 검증 오류는 폼의 `errors` 객체에 자동으로 채워집니다.

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 오류가 있는지 확인하려면 폼의 `hasErrors` 속성을 사용할 수 있습니다.

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

또한 입력값의 이름을 폼의 `valid` 및 `invalid` 함수에 각각 전달하여 해당 입력값이 유효성 검증을 통과했는지 또는 실패했는지 확인할 수 있습니다.

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 폼 입력값은 변경된 뒤 유효성 검증 응답을 받은 후에만 유효하거나 유효하지 않은 것으로 표시됩니다.

앞서 살펴본 것처럼 입력값의 `change` 이벤트에 연결하여 사용자가 입력값과 상호작용할 때 개별 입력값을 유효성 검증할 수 있습니다. 하지만 사용자가 아직 상호작용하지 않은 입력값도 유효성 검증해야 할 수 있습니다. 이는 "wizard"를 만들 때 흔히 필요합니다. 다음 단계로 이동하기 전에 사용자가 상호작용했는지 여부와 관계없이 현재 보이는 모든 입력값을 유효성 검증하고 싶은 경우입니다.

Precognition으로 이를 처리하려면 `validate` 메서드를 호출하면서 유효성 검증할 필드 이름을 `only` 설정 키에 전달해야 합니다. 유효성 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다.

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

폼 제출 요청이 진행 중인지 확인하려면 폼의 `processing` 속성을 살펴보면 됩니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 다시 채우기

위에서 살펴본 사용자 생성 예제에서는 Precognition을 사용하여 실시간 유효성 검증을 수행하고 있습니다. 하지만 폼을 제출할 때는 전통적인 서버 측 폼 제출을 사용하고 있습니다. 따라서 서버 측 폼 제출에서 반환된 "old" 입력값과 유효성 검증 오류가 폼에 채워져야 합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는 XHR을 통해 폼을 제출하고 싶다면 Axios 요청 프로미스를 반환하는 폼의 `submit` 함수를 사용할 수 있습니다.

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
### Axios 설정

Precognition 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용하여 애플리케이션의 백엔드로 요청을 보냅니다. 편의를 위해 애플리케이션에서 필요하다면 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어 `laravel-precognition-vue` 라이브러리를 사용할 때, 애플리케이션의 `resources/js/app.js` 파일에서 각 발신 요청에 추가 요청 헤더를 더할 수 있습니다.

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

또는 애플리케이션에 이미 설정된 Axios 인스턴스가 있다면 Precognition이 해당 인스턴스를 대신 사용하도록 지정할 수 있습니다.

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

<a name="validating-arrays"></a>
## 배열 유효성 검증 (Validating Arrays)

와일드카드를 사용하여 배열 또는 중첩 객체 안의 필드를 유효성 검증할 수 있습니다. 각 `*`는 하나의 경로 세그먼트와 일치합니다.

```js
// Validate email for all users in an array...
form.validate('users.*.email');

// Validate all fields in a profile object...
form.validate('profile.*');

// Validate all fields for all users...
form.validate('users.*.*');
```

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이징 (Customizing Validation Rules)

요청의 `isPrecognitive` 메서드를 사용하면 precognitive 요청 중 실행되는 유효성 검증 규칙을 커스터마이징할 수 있습니다.

예를 들어 사용자 생성 폼에서 비밀번호가 "유출되지 않았는지" 확인하는 검사는 최종 폼 제출 시에만 수행하고 싶을 수 있습니다. precognitive 유효성 검증 요청에서는 비밀번호가 필수이며 최소 8자 이상인지까지만 검증합니다. `isPrecognitive` 메서드를 사용하면 폼 요청에 정의된 규칙을 커스터마이징할 수 있습니다.

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

기본적으로 Laravel Precognition은 precognitive 유효성 검증 요청 중 파일을 업로드하거나 유효성 검증하지 않습니다. 이렇게 하면 큰 파일이 불필요하게 여러 번 업로드되는 것을 방지할 수 있습니다.

이 동작 때문에, 애플리케이션에서 [해당 폼 요청의 유효성 검증 규칙을 커스터마이징](#customizing-validation-rules)하여 해당 필드가 전체 폼 제출에서만 필수임을 지정해야 합니다.

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

모든 유효성 검증 요청에 파일을 포함하고 싶다면 클라이언트 측 폼 인스턴스에서 `validateFiles` 함수를 호출할 수 있습니다.

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부작용 관리 (Managing Side-Effects)

라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때는 precognitive 요청 중 건너뛰어야 하는 부작용이 _다른_ 미들웨어에 있는지 고려해야 합니다.

예를 들어 각 사용자가 애플리케이션에서 수행한 "상호작용" 총 횟수를 증가시키는 미들웨어가 있을 수 있습니다. 하지만 precognitive 요청은 상호작용으로 계산하고 싶지 않을 수 있습니다. 이를 처리하려면 상호작용 횟수를 증가시키기 전에 요청의 `isPrecognitive` 메서드를 확인하면 됩니다.

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

테스트에서 precognitive 요청을 만들고 싶다면 Laravel의 `TestCase`에 포함된 `withPrecognition` 헬퍼를 사용할 수 있습니다. 이 헬퍼는 `Precognition` 요청 헤더를 추가합니다.

또한 precognitive 요청이 성공했는지, 예를 들어 유효성 검증 오류를 반환하지 않았는지 검증하고 싶다면 응답에서 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다.

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
