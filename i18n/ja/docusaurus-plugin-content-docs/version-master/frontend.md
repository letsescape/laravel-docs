# フロントエンド (Frontend)

- [Introduction](#introduction)
- [PHPの使用](#using-php)
    - [PHP とBlade](#php-and-blade)
    - [Livewire](#livewire)
    - [スターターキット](#php-starter-kits)
- [React、Svelte、または Vue の使用](#using-react-svelte-or-vue)
    - [Inertia](#inertia)
    - [スターターキット](#inertia-starter-kits)
- [アセットのバンドル](#bundling-assets)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、[routing](/docs/{{version}}/routing)、[validation](/docs/{{version}}/validation)、[caching](/docs/{{version}}/cache)、[queues](/docs/{{version}}/queues)、[ファイルストレージ](/docs/{{version}}/filesystem) などの最新の Web アプリケーションを構築するために必要なすべての機能を提供するバックエンド フレームワークです。ただし、アプリケーションのフロントエンドを構築するための強力なアプローチを含む、美しいフルスタック エクスペリエンスを開発者に提供することが重要であると私たちは考えています。

Laravel でアプリケーションを構築するときにフロントエンド開発に取り組むには主に 2 つの方法があり、どちらのアプローチを選択するかは、PHP を活用してフロントエンドを構築するか、React、Svelte、Vue などの JavaScript フレームワークを使用してフロントエンドを構築するかによって決まります。アプリケーションのフロントエンド開発への最適なアプローチに関して情報に基づいた決定を行えるように、これらのオプションの両方について以下で説明します。

<a name="using-php"></a>
## PHPの使用 (Using PHP)

<a name="php-and-blade"></a>
### PHP とBlade

以前は、ほとんどの PHP アプリケーションは、リクエスト中にデータベースから取得したデータをレンダリングする PHP `echo` ステートメントが散在する単純な HTML テンプレートを使用して、ブラウザに HTML をレンダリングしていました。

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel では、HTML をレンダリングするこのアプローチは、[views](/docs/{{version}}/views) および [Blade](/docs/{{version}}/blade) を使用して実現できます。 Blade は、データの表示、データの反復処理などに便利な短い構文を提供する非常に軽量なテンプレート言語です。

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

この方法でアプリケーションを構築する場合、フォーム送信やその他のページ操作は通常、サーバーからまったく新しい HTML ドキュメントを受け取り、ページ全体がブラウザーによって再レンダリングされます。現在でも、多くのアプリケーションは、単純な Blade テンプレートを使用してこのようにフロントエンドを構築するのに完全に適している可能性があります。

<a name="growing-expectations"></a>
#### 高まる期待

しかし、Web アプリケーションに対するユーザーの期待が高まるにつれ、多くの開発者は、より洗練された操作性を備えた、より動的なフロントエンドを構築する必要があることに気づきました。これを考慮して、一部の開発者は、React、Svelte、Vue などの JavaScript フレームワークを使用してアプリケーションのフロントエンドの構築を開始することを選択します。

使い慣れたバックエンド言語を使い続けることを好む企業もあり、主に選択したバックエンド言語を利用しながら、最新の Web アプリケーション UI を構築できるソリューションを開発しました。たとえば、[Rails](https://rubyonrails.org/) エコシステムでは、これにより、[Turbo](https://turbo.hotwired.dev/)、[Hotwire](https://hotwired.dev/)、[Stimulus](https://stimulus.hotwired.dev/) などのライブラリの作成が促進されました。

Laravel エコシステム内では、主に PHP を使用して最新の動的なフロントエンドを作成する必要があるため、[Laravel Livewire](https://livewire.laravel.com) および [Alpine.js](https://alpinejs.dev/) が作成されました。

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com) は、React、Svelte、Vue などの最新の JavaScript フレームワークで構築されたフロントエンドと同様に、ダイナミックでモダンで生き生きとした Laravel を利用したフロントエンドを構築するためのフレームワークです。

Livewire を使用する場合、UI の個別の部分をレンダリングし、アプリケーションのフロントエンドから呼び出して操作できるメソッドとデータを公開する Livewire「コンポーネント」を作成します。たとえば、単純な「カウンター」コンポーネントは次のようになります。

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

ご覧のとおり、Livewire を使用すると、Laravel アプリケーションのフロントエンドとバックエンドを接続する `wire:click` などの新しい HTML 属性を作成できます。さらに、単純な Blade 式を使用してコンポーネントの現在の状態をレンダリングできます。

多くの人にとって、Livewire は Laravel を使用したフロントエンド開発に革命をもたらし、最新の動的な Web アプリケーションを構築しながら Laravel の快適さを維持できるようにしました。通常、Livewire を使用する開発者は、[Alpine.js](https://alpinejs.dev/) も利用して、ダイアログ ウィンドウをレンダリングするためなど、必要な場所にのみ JavaScript をフロントエンドに「散布」します。

Laravel を初めて使用する場合は、[views](/docs/{{version}}/views) と [Blade](/docs/{{version}}/blade) の基本的な使用法に慣れることをお勧めします。次に、公式 [Laravel Livewire ドキュメント](https://livewire.laravel.com/docs) を参照して、インタラクティブな Livewire コンポーネントを使用してアプリケーションを次のレベルに引き上げる方法を学習してください。

<a name="php-starter-kits"></a>
### スターターキット

PHP と Livewire を使用してフロントエンドを構築したい場合は、[Livewireスターターキット](/docs/{{version}}/starter-kits) を利用してアプリケーションの開発をすぐに開始できます。

<a name="using-react-svelte-or-vue"></a>
## React、Svelte、または Vue の使用 (Using React, Svelte, or Vue)

Laravel や Livewire を使用して最新のフロントエンドを構築することは可能ですが、多くの開発者は依然として React、Svelte、Vue などの JavaScript フレームワークの力を活用することを好みます。これにより、開発者は、NPM 経由で利用できる JavaScript パッケージとツールの豊富なエコシステムを利用できるようになります。

ただし、追加のツールがなければ、Laravel を React、Svelte、または Vue と組み合わせると、クライアント側のルーティング、データ ハイドレーション、認証などのさまざまな複雑な問題を解決する必要があります。クライアント側のルーティングは、[Next](https://nextjs.org/) や [Nuxt](https://nuxt.com/) などの独自の React / Svelte / Vue フレームワークを使用することで簡素化されることがよくあります。ただし、Laravel などのバックエンド フレームワークをこれらのフロントエンド フレームワークと組み合わせる場合、データ ハイドレーションと認証は依然として複雑で解決しにくい問題です。

さらに、開発者は 2 つの別々のコード リポジトリを維持する必要があり、多くの場合、両方のリポジトリにわたるメンテナンス、リリース、デプロイメントを調整する必要があります。これらの問題は克服できないわけではありませんが、それがアプリケーション開発の生産的または楽しい方法であるとは考えていません。

<a name="inertia"></a>
### Inertia

ありがたいことに、Laravel は両方の長所を提供します。 [Inertia](https://inertiajs.com) は、Laravel アプリケーションと最新の React、Svelte、または Vue フロントエンドの間のギャップを橋渡しし、ルーティング、データ ハイドレーション、認証に Laravel のルートとコントローラを活用しながら、React、Svelte、または Vue を使用して本格的な最新のフロントエンドを構築できるようにします。すべて単一のコード リポジトリ内で行われます。このアプローチを使用すると、Laravel と React / Svelte / Vue の両方の機能を損なうことなく、両方のパワーを最大限に楽しむことができます。

Inertia を Laravel アプリケーションにインストールしたら、通常どおりルートとコントローラを記述します。ただし、コントローラから Blade テンプレートを返す代わりに、Inertia ページを返します。

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

Inertia ページは、React、Svelte、または Vue コンポーネントに対応しており、通常はアプリケーションの `resources/js/pages` ディレクトリ内に保存されます。 `Inertia::render` メソッドを介してページに与えられたデータは、ページ コンポーネントの「プロパティ」をハイドレートするために使用されます。

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

ご覧のとおり、Inertia を使用すると、フロントエンドの構築時に React、Svelte、または Vue の能力を最大限に活用できると同時に、Laravel を利用したバックエンドと JavaScript を利用したフロントエンドの間に軽量のブリッジを提供できます。

#### サーバーサイドレンダリング

アプリケーションにはサーバー側のレンダリングが必要なため、Inertia に飛び込むことに不安がある場合でも、心配する必要はありません。 Inertia は [サーバー側レンダリングのサポート](https://inertiajs.com/server-side-rendering) を提供します。また、[Laravel Cloud](https://cloud.laravel.com) または [Laravel Forge](https://forge.laravel.com) 経由でアプリケーションをデプロイする場合、Inertia のサーバー側レンダリング プロセスが常に実行されていることを確認するのは簡単です。

<a name="inertia-starter-kits"></a>
### スターターキット

Inertia と React / Svelte / Vue を使用してフロントエンドを構築したい場合は、[React、Svelte、または Vue アプリケーション スターター キット](/docs/{{version}}/starter-kits) を活用してアプリケーションの開発を開始できます。これらのスターター キットは両方とも、Inertia、React / Svelte / Vue、[Tailwind](https://tailwindcss.com)、[Vite](https://vitejs.dev) を使用してアプリケーションのバックエンドとフロントエンドの認証フローを足場にするため、次の大きなアイデアの構築を開始できます。

<a name="bundling-assets"></a>
## アセットのバンドル (Bundling Assets)

Blade と Livewire を使用するか、React / Svelte / Vue と Inertia を使用してフロントエンドを開発することを選択するかに関係なく、アプリケーションの CSS を本番環境に対応したアセットにバンドルする必要がある可能性があります。もちろん、React、Svelte、または Vue を使用してアプリケーションのフロントエンドを構築することを選択した場合は、コンポーネントをブラウザー対応の JavaScript アセットにバンドルする必要もあります。

デフォルトでは、Laravel は [Vite](https://vitejs.dev) を利用してアセットをバンドルします。 Vite は、ローカル開発中に超高速なビルド時間とほぼ瞬時のホット モジュール交換 (HMR) を提供します。 [スターターキット](/docs/{{version}}/starter-kits) を使用するものを含むすべての新しい Laravel アプリケーションには、Laravel アプリケーションで Vite を快適に使用できる軽量の Laravel Vite プラグインをロードする `vite.config.js` ファイルがあります。

Laravel と Vite を使い始める最も早い方法は、[当社のアプリケーションスターターキット](/docs/{{version}}/starter-kits) を使用してアプリケーションの開発を開始することです。これにより、フロントエンドとバックエンドの認証スキャフォールディングが提供されてアプリケーションが活性化されます。

> [!NOTE]
> Laravel での Vite の利用に関する詳細なドキュメントについては、[アセットのバンドルとコンパイルに関する専用ドキュメント](/docs/{{version}}/vite) を参照してください。

