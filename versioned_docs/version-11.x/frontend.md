<!-- # Frontend -->
# Frontend

- [Introduction](#introduction)
- [Using PHP](#using-php)
    - [PHP and Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [Starter Kits](#php-starter-kits)
- [Using Vue / React](#using-vue-react)
    - [Inertia](#inertia)
    - [Starter Kits](#inertia-starter-kits)
- [Bundling Assets](#bundling-assets)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is a backend framework that provides all of the features you need to build modern web applications, such as [routing](/docs/11.x/routing), [validation](/docs/11.x/validation), [caching](/docs/11.x/cache), [queues](/docs/11.x/queues), [file storage](/docs/11.x/filesystem), and more. However, we believe it's important to offer developers a beautiful full-stack experience, including powerful approaches for building your application's frontend. -->
Laravel은 [routing](/docs/11.x/routing), [validation](/docs/11.x/validation), [caching](/docs/11.x/cache), [queues](/docs/11.x/queues), [file storage](/docs/11.x/filesystem) 등과 같이 현대적인 웹 애플리케이션 구축에 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만 저희는 개발자에게 아름다운 풀스택 개발 경험을 제공하는 것이 중요하다고 생각하며, 이를 위해 프론트엔드 구축을 위한 강력한 접근법도 함께 제시하고 있습니다.

<!-- There are two primary ways to tackle frontend development when building an application with Laravel, and which approach you choose is determined by whether you would like to build your frontend by leveraging PHP or by using JavaScript frameworks such as Vue and React. We'll discuss both of these options below so that you can make an informed decision regarding the best approach to frontend development for your application. -->
Laravel로 애플리케이션을 개발할 때 프론트엔드 개발을 진행하는 주요 방식은 두 가지입니다. 여러분이 프론트엔드를 PHP로 구현할지, 아니면 Vue나 React 같은 JavaScript 프레임워크를 활용할지에 따라 나뉩니다. 아래에서는 이 두 가지 방식을 모두 다루며, 여러분의 애플리케이션에 가장 적합한 프론트엔드 개발 방식을 결정할 수 있도록 도와드립니다.

<a name="using-php"></a>
<!-- ## Using PHP -->
## Using PHP

<a name="php-and-blade"></a>
<!-- ### PHP and Blade -->
### PHP and Blade

<!-- In the past, most PHP applications rendered HTML to the browser using simple HTML templates interspersed with PHP `echo` statements which render data that was retrieved from a database during the request: -->
과거에는 대부분의 PHP 애플리케이션이 단순 HTML 템플릿 안에 PHP `echo` 문을 삽입하여, 요청 시 데이터베이스에서 가져온 데이터를 브라우저로 렌더링하는 방식이 일반적이었습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

<!-- In Laravel, this approach to rendering HTML can still be achieved using [views](/docs/11.x/views) and [Blade](/docs/11.x/blade). Blade is an extremely light-weight templating language that provides convenient, short syntax for displaying data, iterating over data, and more: -->
Laravel에서도 이러한 방식으로 HTML을 렌더링할 수 있으며, 이는 [views](/docs/11.x/views) 및 [Blade](/docs/11.x/blade)를 활용하여 구현할 수 있습니다. Blade는 매우 가볍고 직관적인 템플릿 언어로, 데이터를 출력하거나 반복 처리하는 작업을 간결한 문법으로 지원합니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

<!-- When building applications in this fashion, form submissions and other page interactions typically receive an entirely new HTML document from the server and the entire page is re-rendered by the browser. Even today, many applications may be perfectly suited to having their frontends constructed in this way using simple Blade templates. -->
이와 같은 방식으로 애플리케이션을 구축하면, 보통 폼 제출이나 페이지 내 상호작용이 있을 때마다 서버에서 HTML 문서 전체를 새로 받아와 브라우저가 전체 페이지를 다시 렌더링합니다. 여전히 많은 애플리케이션에서 간단한 Blade 템플릿만으로도 충분히 프론트엔드를 구축할 수 있습니다.

<a name="growing-expectations"></a>
<!-- #### Growing Expectations -->
#### Growing Expectations

<!-- However, as user expectations regarding web applications have matured, many developers have found the need to build more dynamic frontends with interactions that feel more polished. In light of this, some developers choose to begin building their application's frontend using JavaScript frameworks such as Vue and React. -->
하지만 웹 애플리케이션에 대한 사용자 기대치가 점점 높아지면서, 더 다이내믹하고 세련된 상호작용이 요구되는 프론트엔드를 구축해야 하는 경우가 많아졌습니다. 이런 흐름에 따라 일부 개발자들은 Vue나 React 같은 JavaScript 프레임워크를 이용해 프론트엔드를 제작하기 시작했습니다.

<!-- Others, preferring to stick with the backend language they are comfortable with, have developed solutions that allow the construction of modern web application UIs while still primarily utilizing their backend language of choice. For example, in the [Rails](https://rubyonrails.org/) ecosystem, this has spurred the creation of libraries such as [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/), and [Stimulus](https://stimulus.hotwired.dev/). -->
한편, 익숙한 백엔드 언어에 계속 머물고 싶은 개발자들은 현대적인 웹 UI를 백엔드 언어 위주로 구현할 수 있는 다양한 솔루션을 만들기도 했습니다. 예를 들어, [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리가 등장했습니다.

<!-- Within the Laravel ecosystem, the need to create modern, dynamic frontends by primarily using PHP has led to the creation of [Laravel Livewire](https://livewire.laravel.com) and [Alpine.js](https://alpinejs.dev/). -->
Laravel 생태계에서도 PHP를 위주로 하면서도 현대적이고 동적인 프론트엔드 구성을 위한 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 만들어졌습니다.

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- [Laravel Livewire](https://livewire.laravel.com) is a framework for building Laravel powered frontends that feel dynamic, modern, and alive just like frontends built with modern JavaScript frameworks like Vue and React. -->
[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React 같은 현대 JavaScript 프레임워크로 만든 프론트엔드처럼 동적이고 생동감 있는 Laravel 기반 프론트엔드를 구축할 수 있게 해주는 프레임워크입니다.

<!-- When using Livewire, you will create Livewire "components" that render a discrete portion of your UI and expose methods and data that can be invoked and interacted with from your application's frontend. For example, a simple "Counter" component might look like the following: -->
Livewire를 사용할 때는 UI의 특정 부분을 담당하는 Livewire "컴포넌트"를 정의합니다. 이 컴포넌트는 외부에서 호출하거나 상호작용할 수 있는 메서드와 데이터를 제공하며, 프론트엔드에서 이를 손쉽게 사용할 수 있게 해줍니다. 예를 들어, 간단한 "카운터" 컴포넌트는 다음과 같이 작성될 수 있습니다.

```php
<?php

namespace App\Http\Livewire;

use Livewire\Component;

class Counter extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

<!-- And, the corresponding template for the counter would be written like so: -->
그리고 카운터에 대응하는 템플릿은 다음과 같이 작성할 수 있습니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

<!-- As you can see, Livewire enables you to write new HTML attributes such as `wire:click` that connect your Laravel application's frontend and backend. In addition, you can render your component's current state using simple Blade expressions. -->
보시는 것처럼, Livewire를 사용하면 `wire:click`과 같은 새로운 HTML 속성을 활용해 Laravel 백엔드와 프론트엔드를 직접 연결할 수 있습니다. 그리고 간단한 Blade 표현식을 통해 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

<!-- For many, Livewire has revolutionized frontend development with Laravel, allowing them to stay within the comfort of Laravel while constructing modern, dynamic web applications. Typically, developers using Livewire will also utilize [Alpine.js](https://alpinejs.dev/) to "sprinkle" JavaScript onto their frontend only where it is needed, such as in order to render a dialog window. -->
많은 개발자들에게 Livewire는 Laravel 프론트엔드 개발의 방식에 큰 변화를 가져왔습니다. Laravel의 친숙함을 그대로 유지하면서도 현대적이고 동적인 웹 애플리케이션을 구축할 수 있기 때문입니다. 보통 Livewire를 사용할 때는 [Alpine.js](https://alpinejs.dev/)를 함께 활용하여, 필요한 부분에만 간단히 자바스크립트를 "첨가"할 수 있습니다(예: 다이얼로그 창 구현 등).

<!-- If you're new to Laravel, we recommend getting familiar with the basic usage of [views](/docs/11.x/views) and [Blade](/docs/11.x/blade). Then, consult the official [Laravel Livewire documentation](https://livewire.laravel.com/docs) to learn how to take your application to the next level with interactive Livewire components. -->
Laravel이 처음이라면, 우선 [views](/docs/11.x/views)와 [Blade](/docs/11.x/blade)의 기본 사용법을 익혀보시기 바랍니다. 그 다음, 공식 [Laravel Livewire documentation](https://livewire.laravel.com/docs)에서 상호작용이 가능한 Livewire 컴포넌트로 애플리케이션을 한 단계 더 발전시키는 방법을 확인해보세요.

<a name="php-starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- If you would like to build your frontend using PHP and Livewire, you can leverage our Breeze or Jetstream [starter kits](/docs/11.x/starter-kits) to jump-start your application's development. Both of these starter kits scaffold your application's backend and frontend authentication flow using [Blade](/docs/11.x/blade) and [Tailwind](https://tailwindcss.com) so that you can simply start building your next big idea. -->
PHP와 Livewire를 사용해 프론트엔드를 구축하고자 한다면, Breeze 또는 Jetstream [starter kits](/docs/11.x/starter-kits)을 활용하여 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 스타터 킷들은 [Blade](/docs/11.x/blade)와 [Tailwind](https://tailwindcss.com)를 이용해 백엔드와 프론트엔드의 인증 흐름을 미리 구성해주므로, 여러분은 곧바로 새로운 아이디어를 실현하는 데 집중하실 수 있습니다.

<a name="using-vue-react"></a>
<!-- ## Using Vue / React -->
## Using Vue / React

<!-- Although it's possible to build modern frontends using Laravel and Livewire, many developers still prefer to leverage the power of a JavaScript framework like Vue or React. This allows developers to take advantage of the rich ecosystem of JavaScript packages and tools available via NPM. -->
Laravel과 Livewire만으로도 현대적인 프론트엔드를 만들 수 있지만, 여전히 많은 개발자들은 Vue나 React 같은 JavaScript 프레임워크가 가진 강력한 기능을 선호합니다. 이를 이용하면 NPM을 통해 제공되는 다양한 자바스크립트 패키지와 도구도 적극적으로 활용할 수 있습니다.

<!-- However, without additional tooling, pairing Laravel with Vue or React would leave us needing to solve a variety of complicated problems such as client-side routing, data hydration, and authentication. Client-side routing is often simplified by using opinionated Vue / React frameworks such as [Nuxt](https://nuxt.com/) and [Next](https://nextjs.org/); however, data hydration and authentication remain complicated and cumbersome problems to solve when pairing a backend framework like Laravel with these frontend frameworks. -->
그러나 추가적인 툴링이 없다면, Laravel을 Vue 또는 React와 결합하여 개발할 때 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 여러 복잡한 문제를 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Nuxt](https://nuxt.com/)나 [Next](https://nextjs.org/) 같은 Vue/React 전용 프레임워크를 통해 간단하게 구현할 수 있지만, 데이터 하이드레이션이나 인증은 여전히 번거롭고 까다로운 작업입니다.

<!-- In addition, developers are left maintaining two separate code repositories, often needing to coordinate maintenance, releases, and deployments across both repositories. While these problems are not insurmountable, we don't believe it's a productive or enjoyable way to develop applications. -->
또한, 서버와 프론트엔드를 별개의 코드 저장소로 각각 관리해야 하므로, 유지보수, 릴리스, 배포 등의 작업을 양쪽에서 따로 신경 써야 하는 경우가 많아집니다. 이런 문제들이 극복 불가능한 것은 아니지만, 생산적이거나 즐거운 개발 방식이라고 생각하지는 않습니다.

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- Thankfully, Laravel offers the best of both worlds. [Inertia](https://inertiajs.com) bridges the gap between your Laravel application and your modern Vue or React frontend, allowing you to build full-fledged, modern frontends using Vue or React while leveraging Laravel routes and controllers for routing, data hydration, and authentication — all within a single code repository. With this approach, you can enjoy the full power of both Laravel and Vue / React without crippling the capabilities of either tool. -->
다행히도 Laravel에서는 두 방식의 장점을 모두 누릴 수 있습니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 현대적인 Vue 또는 React 프론트엔드 사이의 간극을 메워줍니다. Inertia를 사용하면 Vue 혹은 React를 최대한 활용해 완성도 높은 프론트엔드를 만들면서도, Laravel 라우트와 컨트롤러를 통해 라우팅, 데이터 하이드레이션, 인증 등을 처리할 수 있습니다. 그리고 이 모든 것이 단일 저장소 내에서 이루어집니다. 이에 따라 프론트엔드와 백엔드 각각의 장점을 온전히 누릴 수 있습니다.

<!-- After installing Inertia into your Laravel application, you will write routes and controllers like normal. However, instead of returning a Blade template from your controller, you will return an Inertia page: -->
Laravel 애플리케이션에 Inertia를 설치한 뒤에는 기존과 마찬가지로 라우트와 컨트롤러를 작성합니다. 단, 컨트롤러에서 Blade 템플릿 대신 Inertia 페이지를 반환하게 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<!-- An Inertia page corresponds to a Vue or React component, typically stored within the `resources/js/Pages` directory of your application. The data given to the page via the `Inertia::render` method will be used to hydrate the "props" of the page component: -->
Inertia 페이지는 Vue 또는 React 컴포넌트이며, 보통 애플리케이션의 `resources/js/Pages` 디렉토리에 저장됩니다. `Inertia::render` 메서드를 통해 전달한 데이터는 해당 페이지 컴포넌트의 "props"로 사용되어 하이드레이션됩니다.

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/vue3';

const props = defineProps(['user']);
</script>

<template>
    <Head title="User Profile" />

    <Layout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Profile
            </h2>
        </template>

        <div class="py-12">
            Hello, {{ user.name }}
        </div>
    </Layout>
</template>
```

<!-- As you can see, Inertia allows you to leverage the full power of Vue or React when building your frontend, while providing a light-weight bridge between your Laravel powered backend and your JavaScript powered frontend. -->
보시는 것처럼, Inertia를 사용하면 프론트엔드 개발 과정에서 Vue나 React의 모든 기능을 누릴 수 있고, 동시에 Laravel 기반 백엔드와 가볍게 연결할 수 있습니다.

<!-- #### Server-Side Rendering -->
#### Server-Side Rendering

<!-- If you're concerned about diving into Inertia because your application requires server-side rendering, don't worry. Inertia offers [server-side rendering support](https://inertiajs.com/server-side-rendering). And, when deploying your application via [Laravel Forge](https://forge.laravel.com), it's a breeze to ensure that Inertia's server-side rendering process is always running. -->
애플리케이션에 서버사이드 렌더링이 꼭 필요한 경우, Inertia를 사용하는 것이 걱정될 수 있으나 걱정하지 않으셔도 됩니다. Inertia는 [server-side rendering support](https://inertiajs.com/server-side-rendering)을 제공합니다. 그리고 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포할 때도 Inertia의 서버사이드 렌더링 프로세스를 항상 원활하게 유지할 수 있습니다.

<a name="inertia-starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- If you would like to build your frontend using Inertia and Vue / React, you can leverage our Breeze or Jetstream [starter kits](/docs/11.x/starter-kits#breeze-and-inertia) to jump-start your application's development. Both of these starter kits scaffold your application's backend and frontend authentication flow using Inertia, Vue / React, [Tailwind](https://tailwindcss.com), and [Vite](https://vitejs.dev) so that you can start building your next big idea. -->
Inertia와 Vue / React를 함께 활용해 프론트엔드를 개발하고 싶다면, Breeze 또는 Jetstream [starter kits](/docs/11.x/starter-kits#breeze-and-inertia)을 활용해 신속하게 애플리케이션 개발을 시작할 수 있습니다. 이 스타터 킷들은 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 활용하여 백엔드와 프론트엔드 인증 플로우를 미리 구성해주기 때문에, 여러분은 바로 새로운 프로젝트 구축에 집중할 수 있습니다.

<a name="bundling-assets"></a>
<!-- ## Bundling Assets -->
## Bundling Assets

<!-- Regardless of whether you choose to develop your frontend using Blade and Livewire or Vue / React and Inertia, you will likely need to bundle your application's CSS into production ready assets. Of course, if you choose to build your application's frontend with Vue or React, you will also need to bundle your components into browser ready JavaScript assets. -->
Blade와 Livewire, 혹은 Vue / React와 Inertia 중 어떤 방식을 선택하더라도, 실제 서비스에 배포하기 위해서는 애플리케이션의 CSS를 번들링하여 최적화된 에셋으로 만들어야 합니다. 또한 Vue나 React로 프론트엔드를 개발하는 경우, 컴포넌트도 브라우저에서 동작할 수 있도록 자바스크립트 에셋으로 번들링해야 합니다.

<!-- By default, Laravel utilizes [Vite](https://vitejs.dev) to bundle your assets. Vite provides lightning-fast build times and near instantaneous Hot Module Replacement (HMR) during local development. In all new Laravel applications, including those using our [starter kits](/docs/11.x/starter-kits), you will find a `vite.config.js` file that loads our light-weight Laravel Vite plugin that makes Vite a joy to use with Laravel applications. -->
Laravel에서는 기본적으로 [Vite](https://vitejs.dev)를 사용해 에셋을 번들링합니다. Vite는 아주 빠른 빌드 속도와 함께, 개발 환경에서 거의 즉각적으로 적용되는 Hot Module Replacement(HMR) 기능을 제공합니다. 모든 신규 Laravel 애플리케이션([starter kits](/docs/11.x/starter-kits)을 사용하는 경우도 포함)에는 `vite.config.js` 파일이 있으며, 여기에 가볍고 직관적으로 사용할 수 있는 Laravel 전용 Vite 플러그인이 로드되어 있어 Vite 활용을 더욱 쉽게 만들어줍니다.

<!-- The fastest way to get started with Laravel and Vite is by beginning your application's development using [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze), our simplest starter kit that jump-starts your application by providing frontend and backend authentication scaffolding. -->
Laravel과 Vite로 개발을 시작하는 가장 빠른 방법은 [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze)를 선택하는 것입니다. Breeze는 가장 간단한 스타터 킷으로, 프론트엔드와 백엔드 인증 플로우까지 미리 구성해두어 바로 애플리케이션 개발을 시작할 수 있습니다.

> [!NOTE]
> Laravel에서 Vite를 활용한 에셋 번들링 및 컴파일 방법에 대한 자세한 설명은 [dedicated documentation on bundling and compiling your assets](/docs/11.x/vite)를 참고하시기 바랍니다.
