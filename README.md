# AstraLua

Cliente derivado do CloakV4, com integração do Antilua e base Luanti 5.17.0.
O projeto busca preservar a aparência do Luanti original, oferecer as funções
em português do Brasil e guardar os dados do jogador em `~/Luanti`.

> **Estado atual: integração em desenvolvimento.** Não há uma versão final
> validada deste fork. A existência de código ou de uma opção no menu não
> significa que a função já foi testada. Consulte o inventário em
> [doc/pt_BR/inventario-cloak.json](doc/pt_BR/inventario-cloak.json).

## Créditos aos projetos originais

- [Luanti](https://github.com/luanti-org/luanti): motor de jogo, interface,
  renderização, rede e infraestrutura de mods; criado por Perttu Ahola
  (celeron55), com contribuições da comunidade.
- [CloakV4 / TeamAcedia](https://github.com/TeamAcedia/CloakV4): origem deste
  fork e de suas funcionalidades próprias. Créditos à equipe TeamAcedia,
  ProunceDev, Maintainer_ / FoxLoveFire, plus22 / Plus-22, Astra0081X,
  Burrowing_Owl e demais colaboradores identificados no histórico.
- [Antilua / corarona](https://github.com/corarona/antilua): extensões da API
  Lua do cliente, ferramentas, módulos, automações e testes de integração.
- Dragonfire, waspsaliva e os demais autores mantêm os créditos registrados
  nos arquivos que forneceram ou inspiraram.

testes e instalações separadas. Não é preciso alterar a variável `HOME`.

## Compilação e distribuição

A compilação pode ser feita localmente em um clique com `./compilar-astralua.sh` ou manualmente no GitHub Actions. Existem somente dois fluxos manuais para Linux: `AstraLua Linux`, que gera o pacote com executável em `bin/` e executa os testes, e `AstraLua AppImage`, que gera o AppImage. Nenhum fluxo é iniciado por push ou pull request. Os detalhes estão em [doc/pt_BR/COMPILAR.md](doc/pt_BR/COMPILAR.md).

## Licenças

O código **novo e independente**, identificado com `SPDX-License-Identifier: MIT`,
usa a [licença MIT](LICENSE-MIT). Essa licença não substitui a licença do código
herdado nem permite remover suas atribuições. Modificações dos arquivos do motor
continuam sujeitas à licença desses arquivos. A distribuição combinada deve
respeitar todas as licenças aplicáveis; o projeto inteiro não é exclusivamente MIT.


O código do motor utiliza LGPL-2.1-ou-posterior. Componentes, mods, fontes,
texturas e sons podem ter licenças próprias. Consulte
[COPYING.LESSER](COPYING.LESSER), [LICENSE.txt](LICENSE.txt) e os avisos dos
respectivos diretórios. Os créditos deste README complementam esses avisos;
não os substituem.
