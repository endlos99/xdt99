// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface Xas99Expr extends PsiElement {

  @NotNull
  List<Xas99Expr> getExprList();

  @Nullable
  Xas99OpAddress getOpAddress();

  @Nullable
  Xas99OpLabel getOpLabel();

}
