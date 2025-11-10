# Maintainer: herdem09 herdem09@proton.me
pkgname=treex
pkgver=1.0.0
pkgrel=1
pkgdesc="TreeX - directory lister with color and summary features"
arch=('x86_64')
url="https://github.com/herdem09/treex"
license=('MIT')
depends=('python')
source=(
    "main.py"
    "README.md"
    "treex.conf"
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    mkdir -p "$pkgdir/usr/bin"
    cp main.py "$pkgdir/usr/bin/treex"
    chmod +x "$pkgdir/usr/bin/treex"

    mkdir -p "$pkgdir/etc/treex"
    cp treex.conf "$pkgdir/etc/treex/"
    
    mkdir -p "$pkgdir/usr/share/doc/treex"
    cp README.md "$pkgdir/usr/share/doc/treex/"
}
