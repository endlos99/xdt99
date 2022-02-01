// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface Xbas99Nexprn extends PsiElement {

  @Nullable
  Xbas99FConst getFConst();

  @Nullable
  Xbas99FNum getFNum();

  @NotNull
  List<Xbas99FStr> getFStrList();

  @NotNull
  List<Xbas99Nexprn> getNexprnList();

  @Nullable
  Xbas99NvarR getNvarR();

  @NotNull
  List<Xbas99Sexpr> getSexprList();

  @NotNull
  List<Xbas99SvarR> getSvarRList();

}
