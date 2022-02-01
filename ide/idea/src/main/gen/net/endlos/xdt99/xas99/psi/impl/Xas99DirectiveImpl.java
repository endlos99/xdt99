// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99.psi.Xas99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99.psi.*;

public class Xas99DirectiveImpl extends ASTWrapperPsiElement implements Xas99Directive {

  public Xas99DirectiveImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99Visitor visitor) {
    visitor.visitDirective(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99Visitor) accept((Xas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xas99ArgsDirC getArgsDirC() {
    return findChildByClass(Xas99ArgsDirC.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirE getArgsDirE() {
    return findChildByClass(Xas99ArgsDirE.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirEO getArgsDirEO() {
    return findChildByClass(Xas99ArgsDirEO.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirES getArgsDirES() {
    return findChildByClass(Xas99ArgsDirES.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirF getArgsDirF() {
    return findChildByClass(Xas99ArgsDirF.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirL getArgsDirL() {
    return findChildByClass(Xas99ArgsDirL.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirR getArgsDirR() {
    return findChildByClass(Xas99ArgsDirR.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirS getArgsDirS() {
    return findChildByClass(Xas99ArgsDirS.class);
  }

  @Override
  @Nullable
  public Xas99ArgsDirT getArgsDirT() {
    return findChildByClass(Xas99ArgsDirT.class);
  }

}
