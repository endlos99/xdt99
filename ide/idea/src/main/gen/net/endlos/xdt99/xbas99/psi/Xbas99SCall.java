// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface Xbas99SCall extends PsiElement {

  @NotNull
  List<Xbas99FStr> getFStrList();

  @NotNull
  List<Xbas99Nexprn> getNexprnList();

  @NotNull
  List<Xbas99Sexpr> getSexprList();

  @NotNull
  Xbas99Subprog getSubprog();

  @NotNull
  List<Xbas99SvarR> getSvarRList();

}
