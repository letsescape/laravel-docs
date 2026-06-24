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
Laravel は、[routing](/docs/11.x/routing)、[validation](/docs/11.x/validation)、[caching](/docs/11.x/cache)、[queues](/docs/11.x/queues)、[file storage](/docs/11.x/filesystem) などの最新の Web アプリケーションを構築するために必要なすべての機能を提供するバックエンド フレームワークです。ただし、アプリケーションのフロントエンドを構築するための強力なアプローチを含む、美しいフルスタック エクスペリエンスを開発者に提供することが重要であると私たちは考えています。

<!-- There are two primary ways to tackle frontend development when building an application with Laravel, and which approach you choose is determined by whether you would like to build your frontend by leveraging PHP or by using JavaScript frameworks such as Vue and React. We'll discuss both of these options below so that you can make an informed decision regarding the best approach to frontend development for your application. -->
Laravel でアプリケーションを構築するときにフロントエンド開発に取り組むには主に 2 つの方法があり、どちらのアプローチを選択するかは、PHP を活用してフロントエンドを構築するか、Vue や React などの JavaScript フレームワークを使用してフロントエンドを構築するかによって決まります。アプリケーションのフロントエンド開発への最適なアプローチに関して情報に基づいた決定を行えるように、これらのオプションの両方について以下で説明します。

<a name="using-php"></a>
<!-- ## Using PHP -->
## Using PHP

<a name="php-and-blade"></a>
<!-- ### PHP and Blade -->
### PHP and Blade

<!-- In the past, most PHP applications rendered HTML to the browser using simple HTML templates interspersed with PHP `echo` statements which render data that was retrieved from a database during the request: -->
以前は、ほとんどの PHP アプリケーションは、リクエスト中にデータベースから取得したデータをレンダリングする PHP `echo` ステートメントが散在する単純な HTML テンプレートを使用して、ブラウザに HTML をレンダリングしていました。

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

<!-- In Laravel, this approach to rendering HTML can still be achieved using [views](/docs/11.x/views) and [Blade](/docs/11.x/blade). Blade is an extremely light-weight templating language that provides convenient, short syntax for displaying data, iterating over data, and more: -->
Laravel では、HTML をレンダリングするこのアプローチは、[views](/docs/11.x/views) および [Blade](/docs/11.x/blade) を使用して実現できます。 Blade は、データの表示、データの反復処理などに便利な短い構文を提供する非常に軽量なテンプレート言語です。

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

<!-- When building applications in this fashion, form submissions and other page interactions typically receive an entirely new HTML document from the server and the entire page is re-rendered by the browser. Even today, many applications may be perfectly suited to having their frontends constructed in this way using simple Blade templates. -->
この方法でアプリケーションを構築する場合、フォーム送信やその他のページ操作は通常、サーバーからまったく新しい HTML ドキュメントを受け取り、ページ全体がブラウザーによって再レンダリングされます。現在でも、多くのアプリケーションは、単純な Blade テンプレートを使用してこのようにフロントエンドを構築するのに完全に適している可能性があります。

<a name="growing-expectations"></a>
<!-- #### Growing Expectations -->
#### Growing Expectations

<!-- However, as user expectations regarding web applications have matured, many developers have found the need to build more dynamic frontends with interactions that feel more polished. In light of this, some developers choose to begin building their application's frontend using JavaScript frameworks such as Vue and React. -->
しかし、Web アプリケーションに対するユーザーの期待が高まるにつれ、多くの開発者は、より洗練された操作性を備えた、より動的なフロントエンドを構築する必要があることに気づきました。これを考慮して、一部の開発者は、Vue や React などの JavaScript フレームワークを使用してアプリケーションのフロントエンドの構築を開始することを選択します。

<!-- Others, preferring to stick with the backend language they are comfortable with, have developed solutions that allow the construction of modern web application UIs while still primarily utilizing their backend language of choice. For example, in the [Rails](https://rubyonrails.org/) ecosystem, this has spurred the creation of libraries such as [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/), and [Stimulus](https://stimulus.hotwired.dev/). -->
使い慣れたバックエンド言語を使い続けることを好む開発者もおり、主に選択したバックエンド言語を利用しながら、最新の Web アプリケーション UI を構築できるソリューションを開発しました。たとえば、[Rails](https://rubyonrails.org/) エコシステムでは、これにより、[Turbo](https://turbo.hotwired.dev/)、[Hotwire](https://hotwired.dev/)、[Stimulus](https://stimulus.hotwired.dev/) などのライブラリの作成が促進されました。

<!-- Within the Laravel ecosystem, the need to create modern, dynamic frontends by primarily using PHP has led to the creation of [Laravel Livewire](https://livewire.laravel.com) and [Alpine.js](https://alpinejs.dev/). -->
Laravel エコシステム内では、主に PHP を使用して最新の動的なフロントエンドを作成する必要があるため、[Laravel Livewire](https://livewire.laravel.com) および [Alpine.js](https://alpinejs.dev/) が作成されました。

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- [Laravel Livewire](https://livewire.laravel.com) is a framework for building Laravel powered frontends that feel dynamic, modern, and alive just like frontends built with modern JavaScript frameworks like Vue and React. -->
[Laravel Livewire](https://livewire.laravel.com) は、Vue や React などの最新の JavaScript フレームワークで構築されたフロントエンドと同様に、ダイナミックでモダンで生き生きとした Laravel を利用したフロントエンドを構築するためのフレームワークです。

<!-- When using Livewire, you will create Livewire "components" that render a discrete portion of your UI and expose methods and data that can be invoked and interacted with from your application's frontend. For example, a simple "Counter" component might look like the following: -->
Livewire を使用する場合、UI の個別の部分をレンダリングし、アプリケーションのフロントエンドから呼び出して操作できるメソッドとデータを公開する Livewire「コンポーネント」を作成します。たとえば、単純な「カウンター」コンポーネントは次のようになります。

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
そして、カウンターに対応するテンプレートは次のように記述されます。

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

<!-- As you can see, Livewire enables you to write new HTML attributes such as `wire:click` that connect your Laravel application's frontend and backend. In addition, you can render your component's current state using simple Blade expressions. -->
ご覧のとおり、Livewire を使用すると、Laravel アプリケーションのフロントエンドとバックエンドを接続する `wire:click` などの新しい HTML 属性を作成できます。さらに、単純な Blade 式を使用してコンポーネントの現在の状態をレンダリングできます。

<!-- For many, Livewire has revolutionized frontend development with Laravel, allowing them to stay within the comfort of Laravel while constructing modern, dynamic web applications. Typically, developers using Livewire will also utilize [Alpine.js](https://alpinejs.dev/) to "sprinkle" JavaScript onto their frontend only where it is needed, such as in order to render a dialog window. -->
多くの人にとって、Livewire は Laravel を使用したフロントエンド開発に革命をもたらし、最新の動的な Web アプリケーションを構築しながら Laravel の快適さを維持できるようにしました。通常、Livewire を使用する開発者は、[Alpine.js](https://alpinejs.dev/) も利用して、ダイアログ ウィンドウをレンダリングするためなど、必要な場所にのみ JavaScript をフロントエンドに「散布」します。

<!-- If you're new to Laravel, we recommend getting familiar with the basic usage of [views](/docs/11.x/views) and [Blade](/docs/11.x/blade). Then, consult the official [Laravel Livewire documentation](https://livewire.laravel.com/docs) to learn how to take your application to the next level with interactive Livewire components. -->
Laravel を初めて使用する場合は、[views](/docs/11.x/views) と [Blade](/docs/11.x/blade) の基本的な使用法に慣れることをお勧めします。次に、公式 [Laravel Livewire documentation](https://livewire.laravel.com/docs) を参照して、インタラクティブな Livewire コンポーネントを使用してアプリケーションを次のレベルに引き上げる方法を学習してください。

<a name="php-starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- If you would like to build your frontend using PHP and Livewire, you can leverage our Breeze or Jetstream [starter kits](/docs/11.x/starter-kits) to jump-start your application's development. Both of these starter kits scaffold your application's backend and frontend authentication flow using [Blade](/docs/11.x/blade) and [Tailwind](https://tailwindcss.com) so that you can simply start building your next big idea. -->
PHP と Livewire を使用してフロントエンドを構築したい場合は、Breeze または Jetstream [starter kits](/docs/11.x/starter-kits) を利用してアプリケーションの開発を開始できます。これらのスターター キットは両方とも、[Blade](/docs/11.x/blade) と [Tailwind](https://tailwindcss.com) を使用してアプリケーションのバックエンドとフロントエンドの認証フローを足場にするため、次の大きなアイデアの構築を簡単に開始できます。

<a name="using-vue-react"></a>
<!-- ## Using Vue / React -->
## Using Vue / React

<!-- Although it's possible to build modern frontends using Laravel and Livewire, many developers still prefer to leverage the power of a JavaScript framework like Vue or React. This allows developers to take advantage of the rich ecosystem of JavaScript packages and tools available via NPM. -->
Laravel や Livewire を使用して最新のフロントエンドを構築することは可能ですが、多くの開発者は依然として Vue や React などの JavaScript フレームワークの力を活用することを好みます。これにより、開発者は、NPM 経由で利用できる JavaScript パッケージとツールの豊富なエコシステムを利用できるようになります。

<!-- However, without additional tooling, pairing Laravel with Vue or React would leave us needing to solve a variety of complicated problems such as client-side routing, data hydration, and authentication. Client-side routing is often simplified by using opinionated Vue / React frameworks such as [Nuxt](https://nuxt.com/) and [Next](https://nextjs.org/); however, data hydration and authentication remain complicated and cumbersome problems to solve when pairing a backend framework like Laravel with these frontend frameworks. -->
ただし、追加のツールがなければ、Laravel と Vue または React を組み合わせると、クライアント側のルーティング、データ ハイドレーション、認証などのさまざまな複雑な問題を解決する必要があります。クライアント側のルーティングは、[Nuxt](https://nuxt.com/) や [Next](https://nextjs.org/) などの独自の Vue / React フレームワークを使用することで簡素化されることがよくあります。ただし、Laravel などのバックエンド フレームワークをこれらのフロントエンド フレームワークと組み合わせる場合、データ ハイドレーションと認証は依然として複雑で解決しにくい問題です。

<!-- In addition, developers are left maintaining two separate code repositories, often needing to coordinate maintenance, releases, and deployments across both repositories. While these problems are not insurmountable, we don't believe it's a productive or enjoyable way to develop applications. -->
さらに、開発者は 2 つの別々のコード リポジトリを維持する必要があり、多くの場合、両方のリポジトリにわたるメンテナンス、リリース、デプロイメントを調整する必要があります。これらの問題は克服できないわけではありませんが、それがアプリケーション開発の生産的または楽しい方法であるとは考えていません。

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- Thankfully, Laravel offers the best of both worlds. [Inertia](https://inertiajs.com) bridges the gap between your Laravel application and your modern Vue or React frontend, allowing you to build full-fledged, modern frontends using Vue or React while leveraging Laravel routes and controllers for routing, data hydration, and authentication — all within a single code repository. With this approach, you can enjoy the full power of both Laravel and Vue / React without crippling the capabilities of either tool. -->
ありがたいことに、Laravel は両方の長所を提供します。 [Inertia](https://inertiajs.com) は、Laravel アプリケーションと最新の Vue または React フロントエンドの間のギャップを橋渡しし、ルーティング、データ ハイドレーション、認証に Laravel ルートとコントローラを活用しながら、Vue または React を使用して本格的な最新のフロントエンドを構築できるようにします。すべて単一のコード リポジトリ内で行われます。このアプローチを使用すると、Laravel と Vue / React の両方の機能を損なうことなく、両方の機能を最大限に活用できます。

<!-- After installing Inertia into your Laravel application, you will write routes and controllers like normal. However, instead of returning a Blade template from your controller, you will return an Inertia page: -->
Inertia を Laravel アプリケーションにインストールしたら、通常どおりルートとコントローラを記述します。ただし、コントローラから Blade テンプレートを返す代わりに、Inertia ページを返します。

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
Inertia ページは Vue または React コンポーネントに対応しており、通常はアプリケーションの `resources/js/Pages` ディレクトリ内に保存されます。 `Inertia::render` メソッドを介してページに与えられたデータは、ページ コンポーネントの「プロパティ」をハイドレートするために使用されます。

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
ご覧のとおり、Inertia を使用すると、Laravel ベースのバックエンドと JavaScript ベースのフロントエンドの間に軽量のブリッジを提供しながら、フロントエンドを構築するときに Vue または React の能力を最大限に活用できます。

<!-- #### Server-Side Rendering -->
#### Server-Side Rendering

<!-- If you're concerned about diving into Inertia because your application requires server-side rendering, don't worry. Inertia offers [server-side rendering support](https://inertiajs.com/server-side-rendering). And, when deploying your application via [Laravel Forge](https://forge.laravel.com), it's a breeze to ensure that Inertia's server-side rendering process is always running. -->
アプリケーションにはサーバー側のレンダリングが必要なため、Inertia に飛び込むことに不安がある場合でも、心配する必要はありません。 Inertia は [server-side rendering support](https://inertiajs.com/server-side-rendering) を提供します。また、[Laravel Forge](https://forge.laravel.com) 経由でアプリケーションをデプロイする場合、Inertia のサーバー側レンダリング プロセスが常に実行されていることを確認するのは簡単です。

<a name="inertia-starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- If you would like to build your frontend using Inertia and Vue / React, you can leverage our Breeze or Jetstream [starter kits](/docs/11.x/starter-kits#breeze-and-inertia) to jump-start your application's development. Both of these starter kits scaffold your application's backend and frontend authentication flow using Inertia, Vue / React, [Tailwind](https://tailwindcss.com), and [Vite](https://vitejs.dev) so that you can start building your next big idea. -->
Inertia と Vue / React を使用してフロントエンドを構築したい場合は、Breeze または Jetstream [starter kits](/docs/11.x/starter-kits#breeze-and-inertia) を利用してアプリケーションの開発をすぐに開始できます。これらのスターター キットは両方とも、Inertia、Vue / React、[Tailwind](https://tailwindcss.com)、[Vite](https://vitejs.dev) を使用してアプリケーションのバックエンドとフロントエンドの認証フローを足場にするため、次の大きなアイデアの構築を開始できます。

<a name="bundling-assets"></a>
<!-- ## Bundling Assets -->
## Bundling Assets

<!-- Regardless of whether you choose to develop your frontend using Blade and Livewire or Vue / React and Inertia, you will likely need to bundle your application's CSS into production ready assets. Of course, if you choose to build your application's frontend with Vue or React, you will also need to bundle your components into browser ready JavaScript assets. -->
Blade と Livewire、または Vue / React と Inertia のどちらを使用してフロントエンドを開発することを選択するかに関係なく、アプリケーションの CSS を実稼働対応のアセットにバンドルする必要がある可能性があります。もちろん、アプリケーションのフロントエンドを Vue または React で構築することを選択した場合は、コンポーネントをブラウザー対応の JavaScript アセットにバンドルする必要もあります。

<!-- By default, Laravel utilizes [Vite](https://vitejs.dev) to bundle your assets. Vite provides lightning-fast build times and near instantaneous Hot Module Replacement (HMR) during local development. In all new Laravel applications, including those using our [starter kits](/docs/11.x/starter-kits), you will find a `vite.config.js` file that loads our light-weight Laravel Vite plugin that makes Vite a joy to use with Laravel applications. -->
デフォルトでは、Laravel は [Vite](https://vitejs.dev) を利用してアセットをバンドルします。 Vite は、ローカル開発中に超高速なビルド時間とほぼ瞬時のホット モジュール交換 (HMR) を提供します。 [starter kits](/docs/11.x/starter-kits) を使用するものを含むすべての新しい Laravel アプリケーションには、Laravel アプリケーションで Vite を快適に使用できる軽量の Laravel Vite プラグインをロードする `vite.config.js` ファイルがあります。

<!-- The fastest way to get started with Laravel and Vite is by beginning your application's development using [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze), our simplest starter kit that jump-starts your application by providing frontend and backend authentication scaffolding. -->
Laravel と Vite を使い始める最も早い方法は、フロントエンドとバックエンドの認証スキャフォールディングを提供する最もシンプルなスターターキットである [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) を使用して、アプリケーションの開発を開始することです。

> [!NOTE]
> Laravel での Vite の利用に関する詳細なドキュメントについては、[dedicated documentation on bundling and compiling your assets](/docs/11.x/vite) を参照してください。

