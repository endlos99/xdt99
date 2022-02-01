// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface Xas99RExpr extends PsiElement {

  @NotNull
  List<Xas99RExpr> getExprList();

  @Nullable
  Xas99ROpAddress getOpAddress();

  @Nullable
  Xas99ROpLabel getOpLabel();

}
