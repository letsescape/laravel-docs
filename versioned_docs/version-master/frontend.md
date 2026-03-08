# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [React, Svelte 또는 Vue 사용하기](#using-react-svelte-or-vue)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [routing](/docs/master/routing), [validation](/docs/master/validation), [caching](/docs/master/cache), [queues](/docs/master/queues), [file storage](/docs/master/filesystem) 등 현대적인 웹 애플리케이션을 구축하는 데 필요한 다양한 기능을 제공하는 백엔드 프레임워크입니다. 그러나 우리는 개발자에게 강력한 프론트엔드 개발 방식까지 포함한 훌륭한 풀스택 경험을 제공하는 것이 중요하다고 생각합니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드를 구현하는 주요 방법은 두 가지가 있습니다. 하나는 **PHP를 활용하여 프론트엔드를 구축하는 방법**이고, 다른 하나는 **React, Svelte, Vue와 같은 JavaScript 프레임워크를 사용하는 방법**입니다. 어떤 접근 방식을 선택할지는 여러분이 어떤 기술 스택으로 프론트엔드를 개발하고 싶은지에 따라 달라집니다. 아래에서는 두 가지 방법을 모두 설명하여 애플리케이션에 가장 적합한 프론트엔드 개발 방식을 선택할 수 있도록 돕겠습니다.

<a name="using-php"></a>
## PHP 사용하기

<a name="php-and-blade"></a>
### PHP와 Blade

과거에는 대부분의 PHP 애플리케이션이 간단한 HTML 템플릿 안에 PHP `echo` 문을 섞어 사용하여 브라우저에 HTML을 렌더링했습니다. 이 `echo` 문은 요청 처리 과정에서 데이터베이스에서 가져온 데이터를 출력하는 역할을 했습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서도 이러한 방식으로 HTML을 렌더링할 수 있으며, 이를 위해 [views](/docs/master/views)와 [Blade](/docs/master/blade)를 사용합니다. Blade는 매우 가벼운 템플릿 언어로, 데이터를 출력하거나 데이터를 반복 처리하는 등의 작업을 더 편리하고 간결한 문법으로 작성할 수 있게 해줍니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이 방식으로 애플리케이션을 만들면, 폼 제출이나 기타 페이지 상호작용이 발생할 때 서버로부터 **완전히 새로운 HTML 문서**를 받아오게 되며, 브라우저는 페이지 전체를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션이 단순한 Blade 템플릿을 사용한 이러한 방식의 프론트엔드 구조에 충분히 잘 맞습니다.

<a name="growing-expectations"></a>
#### 높아지는 기대치

하지만 웹 애플리케이션에 대한 사용자 기대 수준이 높아지면서, 많은 개발자가 더 **동적이고 세련된 상호작용**을 제공하는 프론트엔드를 구축할 필요성을 느끼게 되었습니다. 이러한 이유로 일부 개발자는 React, Svelte, Vue 같은 JavaScript 프레임워크를 사용해 프론트엔드를 개발하기 시작했습니다.

반면, 자신이 익숙한 백엔드 언어를 계속 사용하고 싶어 하는 개발자들도 있습니다. 이들은 여전히 백엔드 언어를 중심으로 사용하면서도 현대적인 웹 애플리케이션 UI를 구축할 수 있는 해결책을 만들었습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리가 등장했습니다.

Laravel 생태계에서도 PHP를 중심으로 현대적이고 동적인 프론트엔드를 만들고자 하는 요구가 생겼고, 그 결과 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 등장했습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Laravel 기반의 프론트엔드를 구축하기 위한 프레임워크로, React, Svelte, Vue 같은 현대적인 JavaScript 프레임워크로 만든 프론트엔드처럼 **동적이고 현대적인 사용자 경험**을 제공할 수 있습니다.

Livewire를 사용할 때는 UI의 특정 부분을 렌더링하는 **Livewire "컴포넌트"**를 생성합니다. 이 컴포넌트는 애플리케이션 프론트엔드에서 호출하거나 상호작용할 수 있는 메서드와 데이터를 제공합니다. 예를 들어 간단한 "Counter" 컴포넌트는 다음과 같이 작성할 수 있습니다.

```php
<?php

use Livewire\Component;

new class extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }
};
?>

<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피 Livewire는 `wire:click`과 같은 새로운 HTML 속성을 사용할 수 있게 해주며, 이를 통해 Laravel 애플리케이션의 프론트엔드와 백엔드를 연결합니다. 또한 간단한 Blade 표현식을 사용해 컴포넌트의 현재 상태를 화면에 렌더링할 수 있습니다.

많은 개발자에게 Livewire는 Laravel 프론트엔드 개발 방식을 크게 바꿔 놓았습니다. Laravel 환경을 유지하면서도 현대적이고 동적인 웹 애플리케이션을 만들 수 있기 때문입니다. 일반적으로 Livewire를 사용하는 개발자는 필요한 부분에서만 JavaScript를 추가하기 위해 [Alpine.js](https://alpinejs.dev/)를 함께 사용합니다. 예를 들어 다이얼로그 창을 표시하는 기능 등에 활용됩니다.

Laravel을 처음 사용하는 경우, 먼저 [views](/docs/master/views)와 [Blade](/docs/master/blade)의 기본 사용법을 익히는 것을 권장합니다. 이후 공식 [Laravel Livewire documentation](https://livewire.laravel.com/docs)을 참고하여 인터랙티브한 Livewire 컴포넌트를 통해 애플리케이션을 한 단계 발전시킬 수 있습니다.

<a name="php-starter-kits"></a>
### 스타터 키트

PHP와 Livewire를 사용하여 프론트엔드를 구축하려는 경우, 애플리케이션 개발을 빠르게 시작할 수 있도록 제공되는 [Livewire starter kit](/docs/master/starter-kits)을 활용할 수 있습니다.

<a name="using-react-svelte-or-vue"></a>
## React, Svelte 또는 Vue 사용하기

Laravel과 Livewire를 사용하여 현대적인 프론트엔드를 구축할 수 있지만, 여전히 많은 개발자는 React, Svelte, Vue와 같은 JavaScript 프레임워크의 강력한 기능을 활용하는 것을 선호합니다. 이를 통해 NPM을 통해 제공되는 풍부한 JavaScript 패키지와 도구 생태계를 활용할 수 있습니다.

하지만 별도의 도구 없이 Laravel과 React, Svelte, Vue를 함께 사용하려면 여러 복잡한 문제를 해결해야 합니다. 예를 들어 **클라이언트 사이드 라우팅(client-side routing)**, **데이터 하이드레이션(data hydration)**, **인증(authentication)**과 같은 문제입니다. 클라이언트 사이드 라우팅은 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/) 같은 프레임워크를 사용하면 비교적 쉽게 해결할 수 있지만, 데이터 하이드레이션과 인증 문제는 여전히 복잡하고 번거롭습니다.

또한 개발자는 **두 개의 별도 코드 저장소(repository)**를 유지해야 하며, 유지보수, 릴리스, 배포 등을 두 저장소 간에 조율해야 하는 경우가 많습니다. 이러한 문제는 해결할 수 없는 것은 아니지만, 우리는 이것이 생산적이거나 즐거운 개발 방식이라고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히 Laravel은 이 두 세계의 장점을 모두 제공하는 방법을 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 React, Svelte, Vue 프론트엔드 사이의 간극을 연결해 주는 도구입니다. 이를 통해 **단일 코드 저장소** 안에서 Laravel의 라우트와 컨트롤러를 활용하면서 React, Svelte, Vue로 현대적인 프론트엔드를 구축할 수 있습니다.

즉, 라우팅, 데이터 하이드레이션, 인증은 Laravel이 담당하고, UI는 React / Svelte / Vue가 담당합니다. 이 접근 방식을 사용하면 Laravel과 React / Svelte / Vue의 강력한 기능을 모두 활용하면서도 어느 한쪽의 기능을 제한하지 않고 사용할 수 있습니다.

Laravel 애플리케이션에 Inertia를 설치한 후에는 평소처럼 라우트와 컨트롤러를 작성합니다. 다만 컨트롤러에서 Blade 템플릿을 반환하는 대신 **Inertia 페이지**를 반환합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): Response
    {
        return Inertia::render('users/show', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 React, Svelte 또는 Vue 컴포넌트에 대응되며, 일반적으로 애플리케이션의 `resources/js/pages` 디렉토리에 저장됩니다. `Inertia::render` 메서드를 통해 전달된 데이터는 페이지 컴포넌트의 `"props"`를 초기화(하이드레이션)하는 데 사용됩니다.

```jsx
import Layout from '@/layouts/authenticated';
import { Head } from '@inertiajs/react';

export default function Show({ user }) {
    return (
        <Layout>
            <Head title="Welcome" />
            <h1>Welcome</h1>
            <p>Hello {user.name}, welcome to Inertia.</p>
        </Layout>
    )
}
```

이처럼 Inertia를 사용하면 React, Svelte, Vue의 강력한 기능을 활용하여 프론트엔드를 구축하면서도 Laravel 기반 백엔드와 JavaScript 기반 프론트엔드를 연결하는 가벼운 브리지 역할을 제공받을 수 있습니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 필요해 Inertia 사용을 고민하고 있다면 걱정할 필요가 없습니다. Inertia는 [server-side rendering support](https://inertiajs.com/server-side-rendering)를 제공합니다. 또한 [Laravel Cloud](https://cloud.laravel.com) 또는 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포하는 경우 Inertia의 서버 사이드 렌더링 프로세스를 항상 실행 상태로 유지하는 것도 매우 간단합니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트

Inertia와 React / Svelte / Vue를 사용해 프론트엔드를 구축하려는 경우, 애플리케이션 개발을 빠르게 시작할 수 있도록 제공되는 [React, Svelte, 또는 Vue application starter kits](/docs/master/starter-kits)을 활용할 수 있습니다. 이 스타터 키트들은 Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용하여 **백엔드와 프론트엔드 인증 흐름(authentication flow)**을 자동으로 구성해 주므로, 바로 애플리케이션 개발을 시작할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링 (Bundling Assets)

Blade와 Livewire를 사용하든, React / Svelte / Vue와 Inertia를 사용하든, 대부분의 경우 애플리케이션의 CSS를 **프로덕션용 에셋**으로 번들링해야 합니다. 또한 React, Svelte, Vue를 사용하는 경우 브라우저에서 실행 가능한 JavaScript 에셋으로 컴포넌트를 번들링해야 합니다.

기본적으로 Laravel은 에셋 번들링을 위해 [Vite](https://vitejs.dev)를 사용합니다. Vite는 매우 빠른 빌드 속도와 로컬 개발 환경에서 거의 즉각적인 Hot Module Replacement(HMR)를 제공합니다. 모든 새로운 Laravel 애플리케이션에는 `vite.config.js` 파일이 포함되어 있으며, 여기에는 Laravel 애플리케이션에서 Vite를 쉽게 사용할 수 있도록 도와주는 경량 Laravel Vite 플러그인이 로드됩니다.

Laravel과 Vite를 가장 빠르게 시작하는 방법은 [application starter kits](/docs/master/starter-kits)을 사용하는 것입니다. 이 스타터 키트는 프론트엔드와 백엔드 인증 스캐폴딩을 함께 제공하여 애플리케이션 개발을 빠르게 시작할 수 있도록 도와줍니다.

> [!NOTE]
> Laravel에서 Vite를 사용하는 더 자세한 내용은 [bundling and compiling your assets](/docs/master/vite) 전용 문서를 참고하시기 바랍니다.