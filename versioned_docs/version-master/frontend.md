<!-- # Frontend -->
# Frontend

- [Introduction](#introduction)
- [Using PHP](#using-php)
    - [PHP and Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [Starter Kits](#php-starter-kits)
- [Using React, Svelte, or Vue](#using-react-svelte-or-vue)
    - [Inertia](#inertia)
    - [Starter Kits](#inertia-starter-kits)
- [Bundling Assets](#bundling-assets)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is a backend framework that provides all of the features you need to build modern web applications, such as [routing](/docs/master/routing), [validation](/docs/master/validation), [caching](/docs/master/cache), [queues](/docs/master/queues), [file storage](/docs/master/filesystem), and more. However, we believe it's important to offer developers a beautiful full-stack experience, including powerful approaches for building your application's frontend. -->
Laravel은 [routing](/docs/master/routing), [validation](/docs/master/validation), [caching](/docs/master/cache), [queues](/docs/master/queues), [file storage](/docs/master/filesystem) 등, 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 갖춘 백엔드 프레임워크입니다. 그러나 Laravel은 개발자에게 강력한 프론트엔드 개발 방식과 아름다운 풀스택 경험까지 제공하는 것이 중요하다고 생각합니다.

<!-- There are two primary ways to tackle frontend development when building an application with Laravel, and which approach you choose is determined by whether you would like to build your frontend by leveraging PHP or by using JavaScript frameworks such as React, Svelte, and Vue. We'll discuss both of these options below so that you can make an informed decision regarding the best approach to frontend development for your application. -->
Laravel로 애플리케이션을 만들 때 프론트엔드 개발을 하는 주요 방법은 두 가지이며, 어떤 방식을 선택할지는 PHP를 활용할지, 아니면 React, Svelte, Vue와 같은 JavaScript 프레임워크를 사용할지에 따라 달라집니다. 아래에서 이 두 가지 접근 방식을 모두 살펴보고, 여러분의 애플리케이션에 가장 잘 맞는 프론트엔드 개발 방식을 선택할 수 있도록 안내하겠습니다.

<a name="using-php"></a>
<!-- ## Using PHP -->
## Using PHP

<a name="php-and-blade"></a>
<!-- ### PHP and Blade -->
### PHP and Blade

<!-- In the past, most PHP applications rendered HTML to the browser using simple HTML templates interspersed with PHP `echo` statements which render data that was retrieved from a database during the request: -->
과거에는 대부분의 PHP 애플리케이션이 데이터베이스에서 데이터를 받아와서, PHP `echo`문이 삽입된 간단한 HTML 템플릿을 렌더링하여 브라우저에 HTML을 출력했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

<!-- In Laravel, this approach to rendering HTML can still be achieved using [views](/docs/master/views) and [Blade](/docs/master/blade). Blade is an extremely light-weight templating language that provides convenient, short syntax for displaying data, iterating over data, and more: -->
Laravel에서는 [views](/docs/master/views)와 [Blade](/docs/master/blade)를 사용해 이와 같은 HTML 렌더링 방식을 여전히 구현할 수 있습니다. Blade는 데이터 표시와 반복 등 다양한 작업을 간단하고 짧은 문법으로 처리할 수 있게 해주는 매우 경량의 템플릿 언어입니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

<!-- When building applications in this fashion, form submissions and other page interactions typically receive an entirely new HTML document from the server and the entire page is re-rendered by the browser. Even today, many applications may be perfectly suited to having their frontends constructed in this way using simple Blade templates. -->
이 방식으로 애플리케이션을 개발할 때, 폼 전송이나 페이지 내 상호작용이 발생하면 서버에서 완전히 새로운 HTML 문서를 받아오며, 브라우저는 전체 페이지를 새로 렌더링합니다. 지금도 많은 애플리케이션에서는 이처럼 단순한 Blade 템플릿만으로도 충분히 프론트엔드를 구성할 수 있습니다.

<a name="growing-expectations"></a>
<!-- #### Growing Expectations -->
#### Growing Expectations

<!-- However, as user expectations regarding web applications have matured, many developers have found the need to build more dynamic frontends with interactions that feel more polished. In light of this, some developers choose to begin building their application's frontend using JavaScript frameworks such as React, Svelte, and Vue. -->
하지만 웹 애플리케이션에 대한 사용자 기대치가 발전함에 따라, 더 세련되고 동적인 프론트엔드를 만들고자 하는 요구가 커졌습니다. 그래서 일부 개발자들은 React, Svelte, Vue 같은 자바스크립트 프레임워크를 이용해 프론트엔드 개발을 시작하기도 합니다.

<!-- Others, preferring to stick with the backend language they are comfortable with, have developed solutions that allow the construction of modern web application UIs while still primarily utilizing their backend language of choice. For example, in the [Rails](https://rubyonrails.org/) ecosystem, this has spurred the creation of libraries such as [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/), and [Stimulus](https://stimulus.hotwired.dev/). -->
반면 익숙한 백엔드 언어(PHP)에 머무르길 원하는 개발자들은, 주요 개발 언어(백엔드 언어)만으로도 현대적인 웹 애플리케이션 UI를 제작할 수 있는 솔루션을 만들어 왔습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 그렇습니다.

<!-- Within the Laravel ecosystem, the need to create modern, dynamic frontends by primarily using PHP has led to the creation of [Laravel Livewire](https://livewire.laravel.com) and [Alpine.js](https://alpinejs.dev/). -->
Laravel 생태계에서는 주로 PHP로 동적이고 현대적인 프론트엔드를 만들 필요성 때문에 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 만들어졌습니다.

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- [Laravel Livewire](https://livewire.laravel.com) is a framework for building Laravel powered frontends that feel dynamic, modern, and alive just like frontends built with modern JavaScript frameworks like React, Svelte, and Vue. -->
[Laravel Livewire](https://livewire.laravel.com)는 Laravel을 기반으로 하면서 React, Svelte, Vue와 같은 최신 JavaScript 프레임워크로 만든 프론트엔드처럼 동적이고 현대적인 UI를 구현할 수 있게 해주는 프레임워크입니다.

<!-- When using Livewire, you will create Livewire "components" that render a discrete portion of your UI and expose methods and data that can be invoked and interacted with from your application's frontend. For example, a simple "Counter" component might look like the following: -->
Livewire를 사용할 때, 여러분은 프론트엔드의 한 부분을 렌더링하고, 메서드와 데이터를 외부에서 사용할 수 있게 하는 "Livewire 컴포넌트"를 만듭니다. 예를 들어, 간단한 "카운터(Counter)" 컴포넌트는 다음과 같이 작성될 수 있습니다:

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

<!-- As you can see, Livewire enables you to write new HTML attributes such as `wire:click` that connect your Laravel application's frontend and backend. In addition, you can render your component's current state using simple Blade expressions. -->
보시는 것처럼, Livewire는 `wire:click`과 같은 HTML 속성을 사용할 수 있게 해서, Laravel 애플리케이션의 프론트엔드와 백엔드를 쉽게 연결해줍니다. 또한, 컴포넌트의 현재 상태를 간단한 Blade 표현식으로 렌더링할 수도 있습니다.

<!-- For many, Livewire has revolutionized frontend development with Laravel, allowing them to stay within the comfort of Laravel while constructing modern, dynamic web applications. Typically, developers using Livewire will also utilize [Alpine.js](https://alpinejs.dev/) to "sprinkle" JavaScript onto their frontend only where it is needed, such as in order to render a dialog window. -->
많은 개발자에게 Livewire는 Laravel에서의 프론트엔드 개발의 패러다임을 바꿔 주었으며, Laravel 환경에 익숙한 채로도 모던하고 동적인 웹 애플리케이션을 만들 수 있도록 해주었습니다. 보통 Livewire로 개발하는 분들은 [Alpine.js](https://alpinejs.dev/)를 함께 사용해서, 예를 들어 다이얼로그 창 렌더링처럼 필요한 곳에만 최소한의 자바스크립트를 추가하곤 합니다.

<!-- If you're new to Laravel, we recommend getting familiar with the basic usage of [views](/docs/master/views) and [Blade](/docs/master/blade). Then, consult the official [Laravel Livewire documentation](https://livewire.laravel.com/docs) to learn how to take your application to the next level with interactive Livewire components. -->
Laravel에 처음 입문하셨다면, 먼저 [views](/docs/master/views)와 [Blade](/docs/master/blade)의 기본 사용법을 익히신 후, 공식 [Laravel Livewire documentation](https://livewire.laravel.com/docs)를 참고해 Livewire 컴포넌트로 상호작용이 가능한 애플리케이션을 만들어 보시길 추천합니다.

<a name="php-starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- If you would like to build your frontend using PHP and Livewire, you can leverage our [Livewire starter kit](/docs/master/starter-kits) to jump-start your application's development. -->
PHP와 Livewire로 프론트엔드를 구축하고 싶다면, [Livewire starter kit](/docs/master/starter-kits)를 이용해 애플리케이션 개발을 더욱 빠르게 시작할 수 있습니다.

<a name="using-react-svelte-or-vue"></a>
<!-- ## Using React, Svelte, or Vue -->
## Using React, Svelte, or Vue

<!-- Although it's possible to build modern frontends using Laravel and Livewire, many developers still prefer to leverage the power of a JavaScript framework like React, Svelte, or Vue. This allows developers to take advantage of the rich ecosystem of JavaScript packages and tools available via NPM. -->
Laravel과 Livewire만으로도 충분히 현대적인 프론트엔드를 만들 수 있으나, 더 많은 개발자들은 여전히 React, Svelte, Vue와 같은 JavaScript 프레임워크가 가진 강력함을 활용하기를 선호합니다. 이런 선택을 통해 개발자는 NPM을 통해 제공되는 다양한 JavaScript 패키지와 툴의 풍부한 생태계를 사용할 수 있습니다.

<!-- However, without additional tooling, pairing Laravel with React, Svelte, or Vue would leave us needing to solve a variety of complicated problems such as client-side routing, data hydration, and authentication. Client-side routing is often simplified by using opinionated React / Svelte / Vue frameworks such as [Next](https://nextjs.org/) and [Nuxt](https://nuxt.com/); however, data hydration and authentication remain complicated and cumbersome problems to solve when pairing a backend framework like Laravel with these frontend frameworks. -->
하지만 추가적인 도구 없이 Laravel을 React, Svelte, Vue와 연동하면, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증(authentication)과 같은 복잡한 문제들을 직접 해결해야 합니다. 클라이언트 사이드 라우팅의 경우에는 [Next](https://nextjs.org/), [Nuxt](https://nuxt.com/) 같은 프레임워크가 해결해 주지만, 데이터 하이드레이션과 인증 문제는 여전히 복잡하고 번거롭게 남습니다.

<!-- In addition, developers are left maintaining two separate code repositories, often needing to coordinate maintenance, releases, and deployments across both repositories. While these problems are not insurmountable, we don't believe it's a productive or enjoyable way to develop applications. -->
또한, 백엔드와 프론트엔드 각각 별도의 코드 저장소를 관리해야 하고, 그에 따른 유지보수나 배포도 별도로 해야 하는 문제가 발생합니다. 이런 문제들은 극복이 불가능한 것은 아니지만, 개발에 있어 생산적이거나 즐거운 방식은 아닙니다.

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- Thankfully, Laravel offers the best of both worlds. [Inertia](https://inertiajs.com) bridges the gap between your Laravel application and your modern React, Svelte, or Vue frontend, allowing you to build full-fledged, modern frontends using React, Svelte, or Vue while leveraging Laravel routes and controllers for routing, data hydration, and authentication — all within a single code repository. With this approach, you can enjoy the full power of both Laravel and React / Svelte / Vue without crippling the capabilities of either tool. -->
다행히도, Laravel은 양쪽의 장점을 모두 누릴 수 있도록 해줍니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 최신 React, Svelte, Vue 프론트엔드 사이를 연결해 주는 다리 역할을 합니다. 이를 통해 라우팅, 데이터 하이드레이션, 인증 등은 Laravel의 라우트와 컨트롤러를 그대로 사용하면서, React, Svelte, Vue로 적극적으로 프론트엔드를 개발할 수 있습니다. 모두 하나의 코드 저장소 내에서 이뤄지며, 두 환경의 장점을 모두 온전히 누릴 수 있습니다.

<!-- After installing Inertia into your Laravel application, you will write routes and controllers like normal. However, instead of returning a Blade template from your controller, you will return an Inertia page: -->
Inertia를 설치한 후, 기존과 동일하게 라우트와 컨트롤러를 작성하면 됩니다. 단, 컨트롤러에서는 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환하게 됩니다:

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

<!-- An Inertia page corresponds to a React, Svelte, or Vue component, typically stored within the `resources/js/pages` directory of your application. The data given to the page via the `Inertia::render` method will be used to hydrate the "props" of the page component: -->
여기서 Inertia 페이지는 React, Svelte, Vue 컴포넌트에 해당하는 것으로, 주로 애플리케이션의 `resources/js/pages` 디렉토리에 저장됩니다. 컨트롤러에서 `Inertia::render`로 넘긴 데이터는 페이지 컴포넌트의 "props"를 채우는 데 사용됩니다:

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

<!-- As you can see, Inertia allows you to leverage the full power of React, Svelte, or Vue when building your frontend, while providing a light-weight bridge between your Laravel powered backend and your JavaScript powered frontend. -->
보시다시피 Inertia를 쓰면, 프론트엔드 개발에 있어 React, Svelte, Vue의 모든 기능을 온전히 활용할 수 있으면서도, Laravel 기반 백엔드와 JavaScript 기반 프론트엔드 사이를 가볍게 연결해주는 역할을 하게 됩니다.

<!-- #### Server-Side Rendering -->
#### Server-Side Rendering

<!-- If you're concerned about diving into Inertia because your application requires server-side rendering, don't worry. Inertia offers [server-side rendering support](https://inertiajs.com/server-side-rendering). And, when deploying your application via [Laravel Cloud](https://cloud.laravel.com) or [Laravel Forge](https://forge.laravel.com), it's a breeze to ensure that Inertia's server-side rendering process is always running. -->
애플리케이션에 서버 사이드 렌더링(Server-Side Rendering)이 필요해서 Inertia 도입이 우려된다면 걱정하지 않으셔도 됩니다. Inertia는 [server-side rendering support](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한, [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)에서 앱을 배포하면 Inertia의 서버 사이드 렌더링 프로세스를 손쉽게 항상 실행되도록 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- If you would like to build your frontend using Inertia and React / Svelte / Vue, you can leverage our [React, Svelte, or Vue application starter kits](/docs/master/starter-kits) to jump-start your application's development. Both of these starter kits scaffold your application's backend and frontend authentication flow using Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com), and [Vite](https://vitejs.dev) so that you can start building your next big idea. -->
Inertia와 React / Svelte / Vue를 활용해 프론트엔드를 만들고 싶으신가요? [React, Svelte, or Vue application starter kits](/docs/master/starter-kits)를 활용해 프로젝트의 개발을 바로 시작해 보세요. 이 스타터 키트들은 Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 이용한 프론트엔드 및 백엔드 인증 플로우 기본 구조를 미리 제공하므로, 여러분의 다음 아이디어 개발에 바로 집중할 수 있습니다.

<a name="bundling-assets"></a>
<!-- ## Bundling Assets -->
## Bundling Assets

<!-- Regardless of whether you choose to develop your frontend using Blade and Livewire or React / Svelte / Vue and Inertia, you will likely need to bundle your application's CSS into production-ready assets. Of course, if you choose to build your application's frontend with React, Svelte, or Vue, you will also need to bundle your components into browser ready JavaScript assets. -->
Blade와 Livewire로 프론트엔드를 개발하든, React / Svelte / Vue와 Inertia로 만들든, 프로덕션 용으로 CSS를 번들링할 필요가 있습니다. 물론, React, Svelte, Vue로 프론트엔드를 만든다면 컴포넌트도 브라우저에서 실행할 수 있는 JavaScript 에셋으로 번들링해야 합니다.

<!-- By default, Laravel utilizes [Vite](https://vitejs.dev) to bundle your assets. Vite provides lightning-fast build times and near instantaneous Hot Module Replacement (HMR) during local development. In all new Laravel applications, including those using our [starter kits](/docs/master/starter-kits), you will find a `vite.config.js` file that loads our light-weight Laravel Vite plugin that makes Vite a joy to use with Laravel applications. -->
Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용해 에셋을 번들링합니다. Vite는 로컬 개발 시 매우 빠른 빌드 속도와 거의 즉각적인 HMR(Hot Module Replacement, 모듈 실시간 교체)을 제공합니다. 신규 Laravel 애플리케이션(모든 [starter kits](/docs/master/starter-kits) 포함)에는 `vite.config.js` 파일이 들어 있으며, Laravel용 경량 Vite 플러그인이 자동으로 로드되어 Vite를 매우 쉽게 사용할 수 있게 도와줍니다.

<!-- The fastest way to get started with Laravel and Vite is by beginning your application's development using [our application starter kits](/docs/master/starter-kits), which jump-starts your application by providing frontend and backend authentication scaffolding. -->
가장 빠르게 Laravel과 Vite를 시작하는 방법은 [our application starter kits](/docs/master/starter-kits)를 이용해 개발을 시작하는 것입니다. 이 스타터 키트는 프론트엔드와 백엔드 인증 구조까지 미리 갖춘 채로 프로젝트를 빠르게 출발할 수 있도록 해줍니다.

> [!NOTE]
> Vite를 Laravel과 함께 활용하는 방법에 대한 더 자세한 설명은 [dedicated documentation on bundling and compiling your assets](/docs/master/vite)를 확인하시기 바랍니다.
